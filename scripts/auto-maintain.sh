#!/usr/bin/env bash
#
# scripts/auto-maintain.sh
#
# Direct-pushes maintenance commits to main with [bot-skip].
set -euo pipefail

REPO_SLUG="aerichmo/grayst0-live-trader"
CLONE_URL="https://${GITHUB_PAT}@github.com/${REPO_SLUG}.git"

WORKDIR="$(mktemp -d)"
BOT_NAME="Grayst0 Bot"
BOT_EMAIL="bot@grayst0.example"
DATE_ISO="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
COMMIT_MSG="chore(bot): automated maintenance ${DATE_ISO} [bot-skip]"

# ── Clone with write creds ───────────────────────────────────────────────────
set +x
git clone --quiet "$CLONE_URL" "$WORKDIR"
cd "$WORKDIR"

# ── Deterministic maintenance actions ────────────────────────────────────────
python -m pip install --quiet --upgrade pip
if [[ -f requirements.in ]]; then
  python -m pip install --quiet pip-tools
  pip-compile --quiet requirements.in --output-file=requirements.txt
fi
python -m pip install --quiet black==24.4.2 isort==5.13.2
isort --quiet . --profile black
black --quiet .

SHORT_SHA="$(git rev-parse --short HEAD)"
echo "$SHORT_SHA" > VERSION

mkdir -p tests/smoke
cat > tests/smoke/test_version.py <<'PY'
import subprocess, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
def test_version_matches_git():
    git_sha = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    file_sha = (ROOT / "VERSION").read_text().strip()
    assert git_sha == file_sha
PY
python -m pip install --quiet -r requirements.txt pytest
pytest -q tests/smoke

# ── Commit & push only if changes exist ──────────────────────────────────────
if git diff --quiet; then
  echo "No changes"
  exit 0
fi

git config user.name  "$BOT_NAME"
git config user.email "$BOT_EMAIL"
git add -A
git commit -m "$COMMIT_MSG"
git push --quiet origin HEAD:main
echo "https://github.com/${REPO_SLUG}/tree/main"
