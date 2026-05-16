#!/usr/bin/env bash
# Send test webhook payloads to the local server.
# Usage: ./scripts/test_local.sh [event]
# Events: issue | pr | comment
# Requires: GITHUB_WEBHOOK_SECRET set in environment or .env

set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"
SECRET="${GITHUB_WEBHOOK_SECRET:-test-secret}"

_sign() {
    echo -n "$1" | openssl dgst -sha256 -hmac "$SECRET" | awk '{print "sha256="$2}'
}

send_event() {
    local event="$1"
    local payload="$2"
    local sig
    sig=$(_sign "$payload")

    echo "→ Sending $event event..."
    curl -s -X POST "$BASE_URL/webhook" \
        -H "Content-Type: application/json" \
        -H "X-GitHub-Event: $event" \
        -H "X-Hub-Signature-256: $sig" \
        -d "$payload" | jq .
}

ISSUE_PAYLOAD='{
  "action": "opened",
  "issue": {
    "number": 99,
    "title": "App crashes on startup",
    "body": "Getting a 500 error when I start the server.",
    "user": {"login": "testuser", "id": 1},
    "labels": []
  },
  "repository": {"id": 1, "full_name": "test-org/test-repo", "default_branch": "main"},
  "installation": {"id": 1}
}'

PR_PAYLOAD='{
  "action": "opened",
  "pull_request": {
    "number": 10,
    "title": "Fix startup crash",
    "body": "Wraps the startup sequence in a try/except.",
    "user": {"login": "contributor", "id": 2}
  },
  "repository": {"id": 1, "full_name": "test-org/test-repo", "default_branch": "main"},
  "installation": {"id": 1}
}'

COMMENT_PAYLOAD='{
  "action": "created",
  "issue": {
    "number": 99,
    "title": "App crashes on startup",
    "body": "Getting a 500 error.",
    "user": {"login": "testuser", "id": 1},
    "labels": [],
    "html_url": "https://github.com/test-org/test-repo/issues/99"
  },
  "comment": {"id": 1, "body": "/copilot help", "user": {"login": "testuser"}},
  "repository": {"id": 1, "full_name": "test-org/test-repo", "default_branch": "main"},
  "installation": {"id": 1}
}'

case "${1:-issue}" in
    issue)   send_event "issues" "$ISSUE_PAYLOAD" ;;
    pr)      send_event "pull_request" "$PR_PAYLOAD" ;;
    comment) send_event "issue_comment" "$COMMENT_PAYLOAD" ;;
    *)       echo "Unknown event: $1. Use: issue | pr | comment" && exit 1 ;;
esac
