"""GitHub Actions script: scans all docs for stale pages and opens GitHub issues.

Usage: python scripts/staleness_notify.py
Requires: GH_TOKEN and REPO environment variables (set by GitHub Actions).
"""

import os
import subprocess
import json
import sys
from datetime import date, datetime
from pathlib import Path

try:
    import frontmatter
except ImportError:
    print("ERROR: Install python-frontmatter: pip install python-frontmatter")
    sys.exit(1)


DOCS_DIR = Path("docs")
LABEL = "stale-doc"
REPO = os.environ.get("REPO", "optimal-living-systems/docs")
GH_TOKEN = os.environ.get("GH_TOKEN", "")


def get_git_last_modified(filepath: str) -> date | None:
    """Get the last commit date for a file from git history."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%aI", "--", filepath],
            capture_output=True,
            text=True,
            check=True,
        )
        if result.stdout.strip():
            return datetime.fromisoformat(result.stdout.strip()).date()
    except (subprocess.CalledProcessError, ValueError):
        pass
    return None


def get_existing_issues() -> set[str]:
    """Get file paths from all open stale-doc issues."""
    try:
        result = subprocess.run(
            [
                "gh", "issue", "list",
                "--repo", REPO,
                "--label", LABEL,
                "--state", "open",
                "--json", "title",
                "--limit", "200",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        issues = json.loads(result.stdout)
        # Convention: issue title starts with "Stale doc: {filepath}"
        return {
            issue["title"].removeprefix("Stale doc: ").strip()
            for issue in issues
        }
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return set()


def create_issue(filepath: str, owner: str, days_overdue: int, review_cycle: int):
    """Create a GitHub issue for a stale page."""
    title = f"Stale doc: {filepath}"
    body = (
        f"## Stale documentation detected\n\n"
        f"**File:** `{filepath}`\n"
        f"**Owner:** {owner}\n"
        f"**Review cycle:** {review_cycle} days\n"
        f"**Days since last update:** {days_overdue}\n\n"
        f"### Action required\n\n"
        f"Page owner: please review this page and either:\n\n"
        f"1. **Confirm accuracy** — update the `created` date in front-matter and close this issue\n"
        f"2. **Update content** — submit a PR with changes (link this issue with `Closes #{{}}`)\n"
        f"3. **Initiate deprecation** — if the page is no longer needed, follow the deprecation protocol\n\n"
        f"See the [Lifecycle Policy](https://docs.optimallivingsystems.org/organization/policies/) for details."
    )
    assignee = owner.lstrip("@") if owner.startswith("@") else ""

    cmd = [
        "gh", "issue", "create",
        "--repo", REPO,
        "--title", title,
        "--body", body,
        "--label", f"{LABEL},documentation",
    ]
    if assignee:
        cmd.extend(["--assignee", assignee])

    try:
        subprocess.run(cmd, check=True)
        print(f"  Created issue: {title}")
    except subprocess.CalledProcessError as e:
        print(f"  ERROR creating issue for {filepath}: {e}")


def main():
    if not GH_TOKEN:
        print("ERROR: GH_TOKEN not set")
        sys.exit(1)

    existing = get_existing_issues()
    today = date.today()
    stale_count = 0
    scanned = 0

    for md_file in sorted(DOCS_DIR.rglob("*.md")):
        scanned += 1
        try:
            post = frontmatter.load(str(md_file))
        except Exception:
            continue

        meta = post.metadata

        # Skip auto-generated, archived, and never-review pages
        if meta.get("generated"):
            continue
        if meta.get("status") == "archived":
            continue

        review_cycle = int(meta.get("review_cycle", 180))
        if review_cycle == 0:
            continue

        # Get last modified from git
        filepath = str(md_file)
        last_modified = get_git_last_modified(filepath)
        if not last_modified:
            # Fallback to created date
            created = meta.get("created")
            if not created:
                continue
            try:
                last_modified = date.fromisoformat(str(created))
            except (ValueError, TypeError):
                continue

        days_since = (today - last_modified).days

        if days_since > review_cycle:
            stale_count += 1
            owner = meta.get("owner", "@ols-documentation-lead")
            rel_path = str(md_file)

            if rel_path in existing:
                print(f"  SKIP (issue exists): {rel_path}")
                continue

            create_issue(rel_path, owner, days_since, review_cycle)

    print(f"\nScan complete: {scanned} files scanned, {stale_count} stale pages found.")


if __name__ == "__main__":
    main()
