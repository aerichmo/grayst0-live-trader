# ---- base image ----
FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Install any OS-level libs you might eventually need
RUN apt-get update && apt-get install -y --no-install-recommends \
        git build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy code and install Python deps (if you have requirements.txt)
WORKDIR /app
COPY requirements.txt ./        # safe even if file doesn’t exist
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy the rest of the repo
COPY . .

CMD [ "python", "-m", "pip", "list" ]  # trivial default command
