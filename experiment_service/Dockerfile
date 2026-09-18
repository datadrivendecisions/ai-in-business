# One container, its own Cloud Run service. SV-11 asks for two deployments
# and no shared container: this is the second, and the Socratic gate's is
# untouched by anything that happens here.
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /srv

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY schema.py store.py app.py server.py ./

# Nothing here needs root.
RUN useradd --create-home --uid 10001 service
USER service

# One worker, a handful of threads. Thirty-two students and a dashboard
# polling every five seconds is not a load problem, and a single worker
# keeps the rate-limit table honest without a shared store behind it.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 30 "app:build()"
