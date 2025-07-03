import os
import requests
import json
from datetime import datetime
from pathlib import Path

USERNAME = os.getenv("LEETCODE_USERNAME", "Psy_Consumer")

RECENT_SUBMISSION_URL = f"https://leetcode.com/api/submissions/{USERNAME}/"

def slug_to_filename(slug):
    return slug.replace("-", "_")

def fetch_recent_submissions():
    response = requests.get(RECENT_SUBMISSION_URL)
    if response.status_code != 200:
        print("❌ Failed to fetch submissions")
        return []
    return response.json().get("submissions_dump", [])

def save_submission(sub):
    title_slug = sub["title_slug"]
    title = sub["title"]
    lang = sub["lang"]
    timestamp = sub["timestamp"]
    code = sub["code"]
    status = sub["status_display"]
    difficulty = "Unknown"

    if status != "Accepted":
        return

    ext_map = {"python3": "py", "cpp": "cpp", "java": "java"}
    ext = ext_map.get(lang.lower(), "txt")

    # Detect difficulty using Leetcode API (optional enhancement)
    problem_info = requests.get(f"https://leetcode.com/api/problems/all/").json()
    for q in problem_info["stat_status_pairs"]:
        if q["stat"]["question__title_slug"] == title_slug:
            diff = q["difficulty"]["level"]
            difficulty = ["Easy", "Medium", "Hard"][diff - 1]
            break

    path = Path(f"{difficulty}/{slug_to_filename(title_slug)}.{ext}")
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(code)
        print(f"✅ Saved: {path}")
    else:
        print(f"⚠️ Already exists: {path}")

def main():
    subs = fetch_recent_submissions()
    for sub in subs:
        save_submission(sub)

    # Save basic stats too
    stats_file = f"stats_{datetime.now().strftime('%Y-%m-%d')}.json"
    with open(stats_file, "w") as f:
        json.dump({"fetched": len(subs)}, f, indent=2)

if __name__ == "__main__":
    main()

