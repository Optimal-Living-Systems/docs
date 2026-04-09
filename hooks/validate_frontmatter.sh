#!/usr/bin/env bash
# validate_frontmatter.sh — Validates YAML front-matter on OLS docs pages
#
# Invoked by Claude Code postWrite hook with: bash hooks/validate_frontmatter.sh $FILE
#
# Exit codes:
#   0 — validation passed
#   1 — validation failed (details printed to stderr)

set -euo pipefail

FILE="${1:-}"

# ---------------------------------------------------------------------------
# FILL: Guard — only validate .md files inside docs/
# ---------------------------------------------------------------------------
# Example logic (to be filled in):
#   if [[ "$FILE" != docs/*.md ]] && [[ "$FILE" != docs/**/*.md ]]; then
#     exit 0
#   fi

# ---------------------------------------------------------------------------
# FILL: Extract YAML front-matter block (between leading --- delimiters)
# ---------------------------------------------------------------------------
# Example logic:
#   FRONTMATTER=$(awk '/^---/{found++; if(found==2) exit} found==1' "$FILE")

# ---------------------------------------------------------------------------
# FILL: Check that front-matter block exists at all
# ---------------------------------------------------------------------------
# Required fields (10 minimum):
#   title, audience, owner, created, review_cycle, status, tags,
#   generated, source_system, summary

# ---------------------------------------------------------------------------
# FILL: Validate each required field is present and non-empty
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# FILL: Validate 'status' is one of: draft | active | review-due | stale | archived
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# FILL: Validate 'audience' is one of: internal | external | both
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# FILL: Validate 'tags' against the controlled vocabulary list
#        (list will be sourced from CLAUDE.md or a separate tags.txt file)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# FILL: Print a summary of all errors, then exit 1 if any were found
# ---------------------------------------------------------------------------

echo "validate_frontmatter.sh: scaffold only — no validation logic yet" >&2
exit 0
