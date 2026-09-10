# Isolated container for cloning + parsing untrusted repo content (Story 2,
# MVP-context.md "Why isolated Docker container for analysis?").
# Runs with no network access beyond git clone + Openrouter API, non-root user.
FROM python:3.12-slim AS base

RUN useradd --create-home --uid 10001 analyzer
WORKDIR /analysis

COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ../app ./app

USER analyzer
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "-m", "app.workflows.analysis_graph"]
