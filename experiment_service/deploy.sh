#!/usr/bin/env bash
# Stand the experiment service up. Read it before you run it: every line
# here costs money or creates something that holds student data.
#
# NOT RUN BY THE BUILD. Deploying is an owner's decision, and this script
# exists so that decision is one command rather than an afternoon.
#
# SV-11 asks for two deployments and no shared container. This creates the
# second one. Nothing here touches the Socratic gate's service, and a bad
# deploy of this cannot take that down.
set -euo pipefail
cd "$(dirname "$0")"          # --source . below means this directory, wherever it is run from

PROJECT="${PROJECT:?set PROJECT to the course cloud project}"
REGION="${REGION:-europe-west4}"          # EU, per ADR-0016
SERVICE="${SERVICE:-experiment-service}"
PAGES_ORIGIN="${PAGES_ORIGIN:-https://datadrivendecisions.github.io}"
DATABASE="${DATABASE:-experiment}"      # its own, never the project's (default)
# The instant every row dies, and the instant the scheduled purge fires: the
# evening of the debrief the data was collected for (ADR-0017). The experiment
# is homework, so rows arrive across a week; they still all go together, and
# this is the date the student read on the page before pressing the button.
# Set it for the cohort you are deploying for, in Amsterdam time.
RETENTION_UNTIL="${RETENTION_UNTIL:-2026-09-28T19:00:00+02:00}"

say() { printf '\n\033[1m== %s\033[0m\n' "$1"; }

say "APIs"
gcloud services enable run.googleapis.com firestore.googleapis.com \
  cloudscheduler.googleapis.com secretmanager.googleapis.com \
  cloudbuild.googleapis.com artifactregistry.googleapis.com --project "$PROJECT"

say "Firestore: a database of its own, in the same EU region"
# Not the project's (default). In the course project that one holds the
# Socratic gate's owner_reports/, which ADR-0015 keeps from anything a student
# can reach -- and this service answers every browser. A named database, and
# a role bound to it alone, make that a permission rather than a habit.
# Named databases are billed from the first read; for one day of thirty-two
# rows that is cents.
if gcloud firestore databases describe --database="$DATABASE" --project "$PROJECT" >/dev/null 2>&1; then
  echo "   $DATABASE already exists; leaving it alone"
else
  gcloud firestore databases create --database="$DATABASE" --location="$REGION" \
    --type=firestore-native --project "$PROJECT"
fi

say "Three secrets"
# The owners' token opens the dashboard and the delete route. The scheduler's
# opens the purge and nothing else, so a job configuration and a person's
# credential are never the same string. The salt makes the dashboard's opaque
# ids unguessable: without it, anyone could hash 'kite' and find that row.
for name in experiment-owner-token experiment-purge-token experiment-id-salt; do
  if ! gcloud secrets describe "$name" --project "$PROJECT" >/dev/null 2>&1; then
    openssl rand -base64 32 | tr -d '\n' \
      | gcloud secrets create "$name" --data-file=- --project "$PROJECT"
    echo "   created $name"
  else
    echo "   $name already exists; leaving it alone"
  fi
done

say "The codebook, as a secret"
# The answer key must never be in the published page (SM-8), and the person
# running the room should not have to paste it. So it sits here, beside the
# owners' token, and the service returns it only inside an owner-authenticated
# dashboard response. Only the card-to-cell pairs go in, not the file's prose.
CODEBOOK_FILE="../work/drafts/week-03-codebook.md"
CODEBOOK="$(python3 - "$CODEBOOK_FILE" <<'PY'
import re, sys
pairs = []
for line in open(sys.argv[1], encoding="utf-8"):
    m = re.search(r"`(c[12]-\d{2})`\s*\|\s*((?:NA|A)(?:S|W)\d*)\s*\|", line)
    if m:
        pairs.append(m.group(1) + " " + m.group(2))
if len(pairs) != 32 or len(set(p.split()[0] for p in pairs)) != 32:
    sys.exit("the codebook should hold 32 distinct cards; found %d" % len(pairs))
print("\n".join(pairs))
PY
)"
if ! gcloud secrets describe experiment-codebook --project "$PROJECT" >/dev/null 2>&1; then
  printf '%s' "$CODEBOOK" | gcloud secrets create experiment-codebook --data-file=- --project "$PROJECT"
  echo "   created experiment-codebook"
elif [ "$(gcloud secrets versions access latest --secret experiment-codebook --project "$PROJECT")" != "$CODEBOOK" ]; then
  printf '%s' "$CODEBOOK" | gcloud secrets versions add experiment-codebook --data-file=- --project "$PROJECT" >/dev/null
  echo "   the codebook changed; added a new version"
else
  echo "   experiment-codebook is current; leaving it alone"
fi

say "A service account that may read and write one database, and no other"
SA="experiment-service@${PROJECT}.iam.gserviceaccount.com"
gcloud iam service-accounts create experiment-service \
  --display-name "Week 3 experiment service" --project "$PROJECT" 2>/dev/null || true
# A new account takes a little while to become visible to IAM, and binding
# it too soon fails with "does not exist". Try for about a minute.
for attempt in 1 2 3 4 5 6; do
  if gcloud projects add-iam-policy-binding "$PROJECT" \
       --member "serviceAccount:$SA" --role roles/datastore.user \
       --condition="expression=resource.name == 'projects/${PROJECT}/databases/${DATABASE}',title=experiment-database-only,description=The week 3 experiment database and nothing else" \
       >/dev/null; then
    break
  fi
  [ "$attempt" = 6 ] && { echo "   the account never became visible to IAM; run this script again"; exit 1; }
  echo "   the new account is not visible to IAM yet; trying again in 10 seconds"
  sleep 10
done
for name in experiment-owner-token experiment-purge-token experiment-id-salt experiment-codebook; do
  gcloud secrets add-iam-policy-binding "$name" --project "$PROJECT" \
    --member "serviceAccount:$SA" --role roles/secretmanager.secretAccessor >/dev/null
done

say "Deploy"
# Unauthenticated, because a student's browser has no identity to present.
# The routes do their own gating: /submit is meant to be open and validates
# every field, and everything else wants a bearer token.
gcloud run deploy "$SERVICE" \
  --source . \
  --project "$PROJECT" \
  --region "$REGION" \
  --service-account "$SA" \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 4 \
  --memory 256Mi \
  --set-env-vars "FIRESTORE_PROJECT=${PROJECT},FIRESTORE_DATABASE=${DATABASE},ALLOWED_ORIGINS=${PAGES_ORIGIN},RETENTION_UNTIL=${RETENTION_UNTIL}" \
  --set-secrets "OWNER_TOKEN=experiment-owner-token:latest,PURGE_TOKEN=experiment-purge-token:latest,ID_SALT=experiment-id-salt:latest,CODEBOOK=experiment-codebook:latest"

URL="$(gcloud run services describe "$SERVICE" --project "$PROJECT" --region "$REGION" --format='value(status.url)')"

say "The purge, on the evening of the debrief"
# Retention is the exercise, not the teaching day (ADR-0017): the experiment is
# homework now, so the rows have to outlive the evening they were sent and die
# on the evening they are shown. The schedule is derived from RETENTION_UNTIL,
# so the deadline lives in one place. This is not the only mechanism -- store.py
# drops an expired row on read and a TTL policy sweeps the rest -- because a
# retention rule that depends on one cron job firing is an intention.
# create takes --headers and update takes --update-headers. The first run
# creates, every later one updates, so a script that only knows --headers
# works once and then fails on the line that matters -- which is how the
# purge stayed on its old schedule through a successful-looking deploy.
PURGE_TOKEN="$(gcloud secrets versions access latest --secret experiment-purge-token --project "$PROJECT")"
# "0 19 28 9 *" from 2026-09-28T19:00:00+02:00: the minute, hour, day and month
# of the deadline, every year. A yearly repeat is harmless -- by then the
# collection it belongs to has been purged once already -- and it keeps the job
# declarative rather than something an owner has to remember to delete.
PURGE_CRON="$(python3 -c "
import datetime, sys
w = datetime.datetime.fromisoformat('${RETENTION_UNTIL}')
print(f'{w.minute} {w.hour} {w.day} {w.month} *')")"
# The scheduler wants a zone name, RETENTION_UNTIL carries an offset. Keep the
# two in step by hand: +02:00 is Amsterdam in September, +01:00 after October.
PURGE_TZ="${PURGE_TZ:-Europe/Amsterdam}"
gcloud scheduler jobs create http experiment-purge \
  --project "$PROJECT" --location "$REGION" \
  --schedule "$PURGE_CRON" --time-zone "$PURGE_TZ" \
  --uri "${URL}/purge" --http-method POST \
  --headers "Authorization=Bearer ${PURGE_TOKEN}" 2>/dev/null \
  || gcloud scheduler jobs update http experiment-purge \
       --project "$PROJECT" --location "$REGION" \
       --schedule "$PURGE_CRON" --time-zone "$PURGE_TZ" \
       --uri "${URL}/purge" --http-method POST \
       --update-headers "Authorization=Bearer ${PURGE_TOKEN}"

say "A TTL policy, for the night the scheduler does not fire"
gcloud firestore fields ttls update expiresAt --database="$DATABASE" \
  --collection-group=submissions --enable-ttl --project "$PROJECT" --quiet \
  || echo "   set the TTL on submissions.expiresAt by hand in the console"

cat <<DONE

Deployed: $URL

Two things left, and neither is in this script:

  1. Put the URL in the tool. One line, in site/tool-bias-experiment.html:
         var SERVICE = { origin: "$URL", ... }
     Until that line changes the page makes no request at all, which is why
     it is safe for this to be deployed before the session and after it.

  2. Read the owners' token, and give it to nobody else:
         gcloud secrets versions access latest \\
           --secret experiment-owner-token --project $PROJECT

DONE
