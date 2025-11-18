import requests
import datetime
import re
import os

TOKEN = os.getenv("GH_TOKEN")

headers = {"Authorization": f"Bearer {TOKEN}"}
USER = "thuleand"

def run_query(query):
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query},
        headers=headers
    )
    data = response.json()
    if "errors" in data:
        print("Erro:", data["errors"])
        raise SystemExit(1)
    return data["data"]["user"]["contributionsCollection"]


# ============================
# 1) Ano atual (Jan → Dez)
# ============================

year = datetime.datetime.now().year
start_year = f"{year}-01-01T00:00:00Z"
end_year = f"{year}-12-31T23:59:59Z"

query_year = f"""
query {{
  user(login: "{USER}") {{
    contributionsCollection(from: "{start_year}", to: "{end_year}") {{
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

data_year = run_query(query_year)
total_year = data_year["contributionCalendar"]["totalContributions"]


# ============================
# 2) Últimos 12 meses (rolling)
# ============================

today = datetime.datetime.utcnow()
last_year_date = today - datetime.timedelta(days=365)

start_rolling = last_year_date.strftime("%Y-%m-%dT%H:%M:%SZ")
end_rolling = today.strftime("%Y-%m-%dT%H:%M:%SZ")

query_rolling = f"""
query {{
  user(login: "{USER}") {{
    contributionsCollection(from: "{start_rolling}", to: "{end_rolling}") {{
      contributionCalendar {{
        totalContributions
      }}
    }}
  }}
}}
"""

data_rolling = run_query(query_rolling)
total_rolling = data_rolling["contributionCalendar"]["totalContributions"]


# ============================
# 3) Atualizar README
# ============================

with open("README.md", "r", encoding="utf8") as f:
    readme = f.read()

new_block = (
    f"<!--STATS-->\n"
    f"**Contribuições em {year}:** {total_year}  \n"
    f"**Contribuições nos últimos 12 meses:** {total_rolling}  \n"
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
