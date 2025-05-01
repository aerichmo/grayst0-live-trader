# ───────── base image ──────────
FROM python:3.11-slim

# ───────── system deps (git, build-essentials) ──────────
RUN apt-get update && apt-get install -y --no-install-recommends \
        git build-essential \
    && rm -rf /var/lib/apt/lists/*

# ───────── app workspace ──────────
WORKDIR /app

# requirements.txt might be empty in early phases – that’s OK
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt || true

# copy the rest of the source tree
COPY . .

# ───────── default test / sanity-check command ──────────
CMD ["python", "-m", "pytest", "-q"]
