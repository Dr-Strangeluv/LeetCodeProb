# fetch_leetcode.py

import requests
import os
import json
from datetime import datetime

USERNAME = os.getenv("LEETCODE_USERNAME", "Psy_Consumer")

QUERY = """
query userProblemsSolved($username: String!) {
  matchedUser(username: $username) {
    submitStats {
      acSubmissionNum {
        difficulty
        count
      }
    }
    problemsSolvedBeatsStats {
      difficulty
      percentage
    }
  }
}
"""

def fetch_solved_problems(username):
    url = "https://leetcode.com/graphql"
    variables = {"username": username}
    response = requests.post(url, json={"query": QUERY, "variables": variables})
    data = response.json()
    return data

def save_to_file(data):
    today = datetime.now().strftime("%Y-%m-%d")
    with open(f"stats_{today}.json", "w") as f:
        json.dump(data, f, indent=4)

def main():
    data = fetch_solved_problems(USERNAME)
    save_to_file(data)

if __name__ == "__main__":
    main()

