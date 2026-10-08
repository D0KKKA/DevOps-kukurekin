#!/usr/bin/env bash
set -euo pipefail

# Creates the required public repository only after verifying the GitHub account email.
EXPECTED_EMAIL="danil.kukurekin@bk.ru"
REPOSITORY="kukurekin-danil-devops"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v gh >/dev/null 2>&1; then
    echo "GitHub CLI is required. Install it, then run: gh auth login"
    exit 1
fi

gh auth status

if ! gh api user/emails --paginate \
    --jq ".[] | select(.email == \"${EXPECTED_EMAIL}\" and .verified == true) | .email" \
    | grep -qx "$EXPECTED_EMAIL"; then
    echo "Refusing to create a repository: the authenticated GitHub account does not expose verified email $EXPECTED_EMAIL."
    echo "Run 'gh auth login' for the personal account, authorize the user:email scope, and try again."
    exit 1
fi

cd "$PROJECT_DIR"
if git remote get-url origin >/dev/null 2>&1; then
    echo "Refusing to overwrite an existing origin remote: $(git remote get-url origin)"
    exit 1
fi

gh repo create "$REPOSITORY" --public --source=. --remote=origin --push
echo "Published: $(git remote get-url origin)"
