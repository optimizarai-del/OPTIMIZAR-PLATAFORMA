import os
import httpx
from typing import List, Dict

def _headers() -> dict:
    token = os.getenv("GITHUB_TOKEN", "")
    h = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def validate_repo(repo: str) -> bool:
    try:
        r = httpx.get(
            f"https://api.github.com/repos/{repo}",
            headers=_headers(), timeout=10,
        )
        return r.status_code == 200
    except Exception:
        return False


def fetch_recent_commits(repo: str, limit: int = 25) -> List[Dict]:
    """Returns list of {sha, message, author, date} for the latest commits."""
    try:
        r = httpx.get(
            f"https://api.github.com/repos/{repo}/commits?per_page={limit}",
            headers=_headers(), timeout=15,
        )
        r.raise_for_status()
        result = []
        for c in r.json():
            result.append({
                "sha": c["sha"][:7],
                "message": c["commit"]["message"].split("\n")[0][:200],
                "author": c["commit"]["author"]["name"],
                "date": c["commit"]["author"]["date"][:10],
            })
        return result
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"GitHub API {e.response.status_code}: {e.response.text[:200]}")
    except Exception as e:
        raise RuntimeError(f"GitHub API error: {e}")


def get_latest_sha(repo: str) -> str | None:
    try:
        commits = fetch_recent_commits(repo, limit=1)
        return commits[0]["sha"] if commits else None
    except Exception:
        return None
