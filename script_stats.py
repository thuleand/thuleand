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
      totalPullRequestContributions
      totalIssueContributions
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

if "errors" in data:
    print("Erro:", data["errors"])
    exit()

stats = data["data"]["user"]["contributionsCollection"]

total_commits = stats["totalCommitContributions"]
total_prs = stats["totalPullRequestContributions"]
total_issues = stats["totalIssueContributions"]

with open("README.md", "r", encoding="utf8") as f:
    readme = f.read()

new_block = (
    f"<!--STATS-->\n"
    f"**Commits em {year}:** {total_commits}  \n"
    f"**PRs em {year}:** {total_prs}  \n"
    f"**Issues em {year}:** {total_issues}\n"
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
