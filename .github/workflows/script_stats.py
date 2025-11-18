import requests
import datetime
import re

TOKEN = None
with open('/github/workflow/event.json', 'r', encoding='utf8') as f:
    pass  

TOKEN = "${{ secrets.GH_TOKEN }}"

headers = {"Authorization": f"Bearer {TOKEN}"}

# Ano atual
year = datetime.datetime.now().year
start = f"{year}-01-01T00:00:00Z"
end = f"{year}-12-31T23:59:59Z"

query = """
query($username: String!) {
  user(login: $username) {
    contributionsCollection(from: "%s", to: "%s") {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
    }
  }
}
""" % (start, end)

response = requests.post(
    "https://api.github.com/graphql",
    json={"query": query, "variables": {"username": "thuleand"}},
    headers=headers
)

data = response.json()
stats = data["data"]["user"]["contributionsCollection"]

total_commits = stats["totalCommitContributions"]
total_prs = stats["totalPullRequestContributions"]
total_issues = stats["totalIssueContributions"]

# Atualiza o README
with open("README.md", "r", encoding="utf8") as f:
    readme = f.read()

readme = re.sub(
    r"<!--STATS-->[\s\S]*<!--STATS-->",
    f"<!--STATS-->\n"
    f"**Commits em {year}:** {total_commits}  \n"
    f"**PRs em {year}:** {total_prs}  \n"
    f"**Issues em {year}:** {total_issues}\n"
    f"<!--STATS-->",
    readme
)

with open("README.md", "w", encoding="utf8") as f:
    f.write(readme)

print("Stats atualizadas!")
