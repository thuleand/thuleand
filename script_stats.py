import requests
import datetime
import re
import os

TOKEN = os.getenv("GH_TOKEN")
USER = "thuleand"

headers = {"Authorization": f"Bearer {TOKEN}"}


def run_query(query):
    resp = requests.post(
        "https://api.github.com/graphql",
        json={"query": query},
        headers=headers,
    )
    data = resp.json()
    print("RAW:", data)  # debug no log do Actions
    if "errors" in data:
        print("Erro:", data["errors"])
        raise SystemExit(1)
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def somar_contribuicoes(calendar):
    total = 0
    for week in calendar["weeks"]:
        for day in week["contributionDays"]:
            total += day["contributionCount"]
    return total


# ============================
# 1) Ano atual (1/jan até hoje)
# ============================

today = datetime.datetime.utcnow()
year = today.year
start_year = datetime.datetime(year, 1, 1)
end_year = today  # até agora

query_year = f"""
query {{
  user(login: "{USER}") {{
    contributionsCollection(from: "{start_year.isoformat()}Z", to: "{end_year.isoformat()}Z") {{
      contributionCalendar {{
        weeks {{
          contributionDays {{
            date
            contributionCount
          }}
        }}
      }}
    }}
  }}
}}
"""

calendar_year = run_query(query_year)
total_year = somar_contribuicoes(calendar_year)


# ============================
# 2) Últimos 12 meses (rolling)
# ============================

inicio_rolling = today - datetime.timedelta(days=365)

query_rolling = f"""
query {{
  user(login: "{USER}") {{
    contributionsCollection(from: "{inicio_rolling.isoformat()}Z", to: "{today.isoformat()}Z") {{
      contributionCalendar {{
        weeks {{
          contributionDays {{
            date
            contributionCount
          }}
        }}
      }}
    }}
  }}
}}
"""

calendar_rolling = run_query(query_rolling)
total_rolling = somar_contribuicoes(calendar_rolling)


# ============================
# 3) Atualizar README
# ============================

with open("README.md", "r", encoding="utf8") as f:
    readme = f.read()

new_block = (
    f"<!--STATS-->\n"
    f"**Contribuições em {year} (soma de todos os dias do ano):** {total_year}  \n"
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
