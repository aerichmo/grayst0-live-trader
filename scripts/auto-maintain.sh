#!/usr/bin/env bash
set -euxo pipefail      # <- add the   -x   (trace)
#!/usr/bin/env bash
set -euo pipefail

echo "🔧 auto‑maintenance started …"

# 1. ensure required CLIs
pip install --quiet --upgrade black isort ruamel.yaml

# 2. run formatters / linters
black .          --quiet
isort .          --quiet

# 3. open a pull‑request if anything changed
if [[ -n "$(git status --porcelain)" ]]; then
  echo "📄 committing code‑style fixes"
  git config --global --add safe.directory "$PWD"
  git add -A
  git commit -m "style: automated formatting by Cloud Build"
  git push origin HEAD:autofix/"${SHORT_SHA:-manual}"

  echo "🔗 creating PR …"
  gh pr create --fill --head "autofix/${SHORT_SHA:-manual}"
else
  echo "✅ nothing to fix"
fi
