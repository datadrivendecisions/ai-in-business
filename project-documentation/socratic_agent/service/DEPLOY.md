# Deploying the weekly gate

> **Deployed 6 September 2026.** Project `ai-in-business-507819`, region `europe-west4`, service
> `socratic-gate`, five scheduler jobs for weeks 2–6 **created and paused**. The roster holds the
> two test fixtures, not a cohort. What remains before it can run for real: replace the roster,
> unpause the weeks, set a budget, and add a second owner to the project.

ADR-0014's scheduled pull, with the parts named: Firestore holds the roster the record calls
infrastructure, Cloud Scheduler is the clock, and Cloud Run runs the agent. Nothing about the
architecture changes — the agent's only input is still a page that is already public, which is what
keeps NFR-11 a property of the wiring rather than a rule a tired student has to remember.

**The schedule is the deadline.** There is no endpoint that runs a team on request except
`?team=`, which exists for a broken run rather than for a late page. Keep it that way: an
instructor who can re-run on request will be asked to, every week, by the team that missed it.

## Decide these before you type anything

- **Which project.** ADR-0009 says the gate runs on a course-owned key with a spend cap. The pilot
  borrowed `ai-consultant-dev`; real student work should not. Whoever owns the project owns the
  gate, and today that is a personal Gmail account (ADR-0014's ownership consequence).
- **Which region.** `europe-west4` for both Firestore and Cloud Run answers the residency question
  the PRD has carried open since ADR-0014. Firestore's location cannot be changed after creation.
- **The budget.** There is no per-agent cap and Cloud Billing alerts rather than stops. Set the
  budget when you enable billing, and know it is a monitored ceiling and not a hard one.

## Once

```bash
PROJECT=<the course project>
REGION=europe-west4

gcloud config set project "$PROJECT"
gcloud services enable run.googleapis.com firestore.googleapis.com \
  cloudscheduler.googleapis.com aiplatform.googleapis.com

gcloud firestore databases create --location="$REGION"

# Least privilege, and the split is the reason: this account writes both
# collections, and the job that delivers reports to teams gets reports/ only.
gcloud iam service-accounts create socratic-gate --display-name="Socratic gate"
SA="socratic-gate@$PROJECT.iam.gserviceaccount.com"
for role in roles/datastore.user roles/aiplatform.user; do
  gcloud projects add-iam-policy-binding "$PROJECT" --member="serviceAccount:$SA" --role="$role"
done
```

## The roster

One document per team in `teams`, id as you want the team named in reports:

```bash
gcloud firestore documents create teams/team-01 \
  --data='{"url":{"stringValue":"https://<team-01 page>"},
           "name":{"stringValue":"Team 1"},
           "active":{"booleanValue":true}}'
```

A team that renames its page silently stops being read, so the roster needs an owner and a check
before each run — ADR-0014 names this and does not solve it.

## Deploy

```bash
gcloud run deploy socratic-gate \
  --source project-documentation/socratic_agent \
  --region "$REGION" --service-account "$SA" --no-allow-unauthenticated \
  --set-env-vars GOOGLE_GENAI_USE_VERTEXAI=TRUE,GOOGLE_CLOUD_PROJECT="$PROJECT",GOOGLE_CLOUD_LOCATION="$REGION" \
  --timeout 900 --memory 1Gi
```

`--no-allow-unauthenticated` matters: an open endpoint is one anybody can run, and the whole
protocol rests on it running once.

## The clock

```bash
URL=$(gcloud run services describe socratic-gate --region "$REGION" --format='value(status.url)')

gcloud scheduler jobs create http socratic-gate-week-02 \
  --location "$REGION" --schedule "0 7 * * MON" --time-zone "Europe/Amsterdam" \
  --uri "$URL/run?week=2" --http-method POST \
  --oidc-service-account-email "$SA" --oidc-token-audience "$URL"
```

One job per teaching week, weeks 2 to 6. Put it far enough after the publication deadline and far
enough before the weekly block that a team can act on the report in the session (NFR-04).

The service returns **500 if any team got no report**, so a failed run shows in the scheduler's
history rather than passing quietly. That is the weekly confirmation the PRD asks for; someone still
has to look.

## Delivering the reports

Not built, and deliberately separate. Whatever reads `reports` and posts to a team's Teams channel
must not be granted `owner_reports` — the collections are split so that a permission boundary does
the work rather than a careful person. The one unrecoverable mistake in this system is the owners'
half reaching a student.

## Checking it before a cohort sees it

Point the roster at the test fixtures and run week 2 by hand:

```bash
gcloud run services proxy socratic-gate --region "$REGION" &
curl -X POST "http://localhost:8080/run?week=2"
```

Expect team 03 to score low with a NOT-FOUND in its ledger, team 07 to score 2–3 with everything
confirmed. `../../test-fixtures/README.md` holds what each fixture should produce.

## The state as deployed

| | |
|---|---|
| Project | `ai-in-business-507819` (349006826805) |
| Region | `europe-west4`, Firestore and Cloud Run both |
| Service | `socratic-gate`, `--no-allow-unauthenticated` |
| Service account | `socratic-gate@…`, `datastore.user` + `aiplatform.user` + `run.invoker` |
| Schedule | Mondays 07:00 Europe/Amsterdam, weeks 2–6, **paused** |
| Roster | two test fixtures |

Verified end to end on deployment: `POST /run?week=2` produced a report for each fixture, the weak
page scoring 1/1/1 and the strong page 2/3/2, and the two halves landed in `reports/` and
`owner_reports/` with no score, ledger word or gate signal anywhere in the team-facing documents.

The jobs are paused because the roster is fixtures. A job that fires on a Monday nobody expects is
noise, and noise teaches people to ignore the thing that is supposed to tell them a run failed.

### Before a cohort

1. Replace the roster: one `teams/{id}` document per team, `url` + `name` + `active: true`. Delete
   the two `fixture-*` documents, and the reports they produced.
2. `gcloud scheduler jobs resume socratic-gate-week-NN --location=europe-west4` per week, once the
   publication deadline that week's run sits behind is agreed and on the week page.
3. Set a budget on the project. Cloud Billing alerts rather than stops, so this is the monitored
   ceiling ADR-0009 asks for and not the hard cap it promises.
4. Add a second owner. The project has one, and it is a personal account — ADR-0015's ownership
   consequence, now holding a database of student work.
5. Build the delivery job, granted `reports/` and refused `owner_reports/`.
