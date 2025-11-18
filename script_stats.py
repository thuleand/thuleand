import requests
import datetime
import re
import os

TOKEN = os.getenv("GH_TOKEN")

headers = {"Authorization": f"Bearer {TOKEN}"}

# Ano atual
year = datetime.datetime.now().year
start = f"{year}-01-01T00:00:00Z"
end = f"{year}-12-31T23:59:59Z"

query = f"""
query {{
  user(login: "thuleand") {{
    contributionsCollection(from: "{start}", to: "{end}") {{
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
      
      contributionCalendar {{
        totalContributions
      }}
    }}
  }}
}}
"""

response = requests.post(
    "https://api.github.com/graphql",
    json={"query": query},
    headers=headers
)

data = response.json()
print("RAW:", data)  # debug

if "errors" in data:
    print("Erro:", data["errors"])
    raise SystemExit(1)

col = data["data"]["user"]["contributionsCollection"]

commits = col["totalCommitContributions"]
issues = col["totalIssueContributions"]
prs = col["totalPullRequestContributions"]
reviews = col["totalPullRequestReviewContributions"]
total = col["contributionCalendar"]["totalContributions"]

with open("README.md", "r", encoding="utf8") as f:
    readme = f.read()

new_block = (
    f"<!--STATS-->\n"
    f"**Contribuições totais em {year} (igual ao gráfico verde):** {total}  \n"
    f"**Commits:** {commits}  \n"
    f"**PRs:** {prs}  \n"
    f"**Issues:** {issues}  \n"
    f"**Reviews:** {reviews}  \n"
    f"<!--STATS-->"
)

readme = re.sub(
    r"<!--STATS-->[\s\S]*<!--STATS-->",
    new_block,
    readme
)

with open("README.md", "w", encoding="utf8") as f:
    f.write(readme)

print("Stats atualizadas!")
