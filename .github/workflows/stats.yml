name: Atualizar Stats Reais

on:
  schedule:
    - cron: "0 3 * * *"   # roda todo dia às 03:00
  workflow_dispatch:       # permite rodar manualmente

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          token: ${{ secrets.GH_TOKEN }}

      - name: Instalar Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Instalar dependências
        run: pip install requests

      - name: Executar script
        run: python script_stats.py

      - name: Commit e Push
        run: |
          git config --global user.name "GitHub Actions"
          git config --global user.email "actions@github.com"
          git add README.md
          git commit -m "Atualizando stats automáticos" || echo "Nada para atualizar"
          git push
