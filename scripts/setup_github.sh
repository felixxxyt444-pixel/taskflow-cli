#!/usr/bin/env bash
# Автор репозитория запускает ОДИН раз. Нужен GitHub CLI: https://cli.github.com  (gh auth login)
# Использование: bash scripts/setup_github.sh taskflow-cli <логин-второго-участника>
set -e
REPO="${1:-taskflow-cli}"
PARTNER="$2"

git init -b main
git add . && git commit -m "docs: начальная структура проекта, README и .gitignore"
gh repo create "$REPO" --public --source=. --push
[ -n "$PARTNER" ] && gh api -X PUT "repos/{owner}/$REPO/collaborators/$PARTNER" -f permission=push

git checkout -b develop && git push -u origin develop

# Метки приоритета MoSCoW
gh label create Must   --color d73a4a --force
gh label create Should --color fbca04 --force
gh label create Could  --color 0e8a16 --force
gh label create review --color 5319e7 --force

# Issues = backlog (по строке из issues.tsv)
while IFS=$'\t' read -r id title meta; do
  prio="${meta%%,*}"
  gh issue create --title "$id $title" --label "$prio" --body "Оценка: ${meta#*,}. Критерий приёмки смотри в отчёте (таблица backlog)."
done < scripts/issues.tsv

echo "Готово. Дальше: создайте доску (Projects → New project → Board) и колонки To Do / In Progress / Code Review / Done."
