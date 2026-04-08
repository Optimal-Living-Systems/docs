"""MkDocs hook: injects stale-page warnings at build time.

Compares each page's last git-modified date against its review_cycle.
Pages past their review window get an admonition inserted above content.

Skips: auto-generated pages, archived pages, pages with review_cycle: 0.
"""

from datetime import date, timedelta

STALE_ADMONITION = """
!!! warning "This page may be outdated"
    This page was last reviewed more than {days} days ago.
    If you find inaccurate information, please [open an issue]({issue_url})
    or contact the page owner: {owner}.

"""


def on_page_markdown(markdown, page, config, **kwargs):
    meta = page.meta

    # Skip auto-generated and archived pages
    if meta.get("generated") or meta.get("status") == "archived":
        return markdown

    review_cycle = int(meta.get("review_cycle", 180))

    # review_cycle: 0 means "never review" (ADRs, meeting notes)
    if review_cycle == 0:
        return markdown

    created = meta.get("created")
    owner = meta.get("owner", "the Documentation Lead")

    if not created:
        return markdown

    try:
        created_date = date.fromisoformat(str(created))
    except (ValueError, TypeError):
        return markdown

    # Use page's source file modification date from git if available
    # Falls back to created date if git info not present
    last_modified = created_date
    if hasattr(page, "meta") and "git_revision_date_localized_raw_datetime" in page.meta:
        try:
            raw = page.meta["git_revision_date_localized_raw_datetime"]
            last_modified = raw.date() if hasattr(raw, "date") else created_date
        except (AttributeError, TypeError):
            pass

    days_since = (date.today() - last_modified).days

    if days_since > review_cycle:
        repo_url = config.get("repo_url", "https://github.com/optimal-living-systems/docs")
        issue_url = repo_url.rstrip("/") + "/issues/new"
        warning = STALE_ADMONITION.format(
            days=review_cycle,
            issue_url=issue_url,
            owner=owner,
        )
        return warning + markdown

    return markdown
