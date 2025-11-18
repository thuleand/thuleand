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

# Agora pedimos contribuições privadas também
query = f"""
query {{
  user(login: "thuleand") {{
    contributionsCollection(from: "{start}", to: "{end}", includePrivateContributions: true) {{
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalPullRequestReviewContributions
      restrictedContributionsCount
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
print("RAW:", data)  # debug se quiser ver algo no log

if "errors" in data:
    print("Erro:", data["errors"])
    raise SystemExit(1)

stats = data["data"]["user"]["contributionsCollection"]

total_commits = stats["totalCommitContributions"]
total_prs = stats["totalPullRequestContributions"]
total_issues = stats["totalIssueContributions"]
total_reviews = stats["totalPullRequestReviewContributions"]
restricted = stats["restrictedContributionsCount"]
calendar_total = stats["contributionCalendar"]["totalContributions"]

with open("README.md", "r", encoding="utf8") as f:
    readme = f.read()

new_block = (
    f"<!--STATS-->\n"
    f"**Contribuições totais em {year} (mesmo número do gráfico verde):** {calendar_total}  \n"
    f"**Commits em {year} (públicos + privados):** {total_commits}  \n"
    f"**PRs em {year}:** {total_prs}  \n"
    f"**Issues em {year}:** {total_issues}  \n"
    f"**Code reviews em {year}:** {total_reviews}  \n"
    f"**Contribuições privadas (não detalhadas):** {restricted}\n"
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
