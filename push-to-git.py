#!/usr/bin/env python3
import subprocess
import os
import sys
import base64
import json
from datetime import datetime
import io

try:
    import requests
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "requests", "-q"], check=True)
    import requests

# Set UTF-8 output encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

DEPLOY_DIR = 'C:\\Users\\maxim\\ClaudeOS\\Content\\deploy'
sys.path.insert(0, DEPLOY_DIR)
from _secrets import GITHUB_TOKEN, GITHUB_REPO  # noqa: E402  (gitignored file)

# JSON files that must be synced to `main` (GitHub Pages branch)
SYNC_FILES = [
    "content-ideas.json",
    "content-analyzed.json",
    "content-titles.json",
    "content-captions.json",
    "content-carousels.json",
    "content-feed.json",
    "content-improver.json",
    "content-caption-analysis.json",
    "content-title-analyzer.json",
]

os.chdir(DEPLOY_DIR)


def sync_file_to_main(filename: str) -> bool:
    """Push a single file to the `main` branch via GitHub API."""
    filepath = os.path.join(DEPLOY_DIR, filename)
    if not os.path.exists(filepath):
        return True  # skip missing files silently

    with open(filepath, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode("utf-8")

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{filename}"

    # Get current SHA on main
    r = requests.get(api_url, headers=headers, params={"ref": "main"})
    sha = r.json().get("sha") if r.status_code == 200 else None

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    payload = {
        "message": f"Sync {filename} to main [{timestamp}]",
        "content": content_b64,
        "branch": "main",
    }
    if sha:
        payload["sha"] = sha

    put = requests.put(api_url, headers=headers, json=payload)
    return put.status_code in (200, 201)


try:
    # ── 1. Push to master ────────────────────────────────────────────────────
    print("Adding files to git...")
    subprocess.run(['git', 'add', '.'], check=True)
    print("✓ Files added")

    status = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
    if status.stdout.strip():
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        subprocess.run(['git', 'commit', '-m', f'Auto-deploy: Update content files [{timestamp}]'], check=True)
        print("✓ Commit created")
        subprocess.run(['git', 'push', 'origin', 'master'], check=True)
        print("✓ Pushed to master")
    else:
        print("✓ No changes to commit on master")

    # ── 2. Sync JSON files to main (GitHub Pages branch) ────────────────────
    print("\nSyncing JSON files to main branch...")
    ok_count = 0
    for fname in SYNC_FILES:
        if sync_file_to_main(fname):
            print(f"  ✓ {fname}")
            ok_count += 1
        else:
            print(f"  ⚠ {fname} — sync failed")

    print(f"\n✅ Synced {ok_count}/{len(SYNC_FILES)} files to main")
    print("Dashboard will update within ~30 seconds:")
    print("  → https://alficcimo.github.io/dashboard/")

except subprocess.CalledProcessError as e:
    print(f"❌ Git error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
