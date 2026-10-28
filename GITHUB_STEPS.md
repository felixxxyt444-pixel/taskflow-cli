# Пошаговый сценарий работы через GitHub (команда из 2 человек)

Участник A = автор репозитория, участник B = второй участник.

## 0. Подготовка (A)
```bash
gh auth login
bash scripts/setup_github.sh taskflow-cli <логин-B>
```
Затем на GitHub: вкладка **Projects → New project → Board**, переименуйте колонки:
`To Do → In Progress → Code Review → Done`. Добавьте issues (Add item). Для WIP-лимита
в настройках колонки "In Progress" укажите лимит 2 на человека (или запишите правило в README).
Включите защиту веток: **Settings → Branches → Add rule** для `main` и `develop`
(Require a pull request before merging, Require approvals = 1).

## 1. Клонирование (B)
```bash
git clone https://github.com/<логин-A>/taskflow-cli.git && cd taskflow-cli
git checkout develop
```

## 2. Разработка и pull request’ы
**A (TASK-1 add):**
```bash
git checkout develop && git pull
git checkout -b feature/TASK-1-add-task
# отредактируйте taskflow/todo.py или добавьте тесты
git commit -am "feat: добавить функцию add() с валидацией (TASK-1)"
git commit -am "test: тесты на добавление задачи (TASK-1)"
git push -u origin feature/TASK-1-add-task
gh pr create --base develop --title "feat: добавление задачи (TASK-1)" --body "Closes #1. Реализована add(), проверка пустого названия, тесты."
```
**B (TASK-4 delete):**
```bash
git checkout develop && git pull
git checkout -b feature/TASK-4-delete-task
git commit -am "feat: добавить функцию удаления задачи (TASK-4)"
git commit -am "test: тест удаления несуществующей задачи (TASK-4)"
git push -u origin feature/TASK-4-delete-task
gh pr create --base develop --title "feat: удаление задачи (TASK-4)" --body "Closes #4. Реализована delete(), KeyError для неизвестного id."
```
Перетаскивайте карточки: To Do → In Progress → Code Review.

## 3. Код-ревью (на сайте GitHub)
Открыть PR другого → **Files changed** → нажать «+» у строки → оставить комментарий →
**Review changes → Approve** (или Request changes) → **Merge pull request** → карточка в Done.

## 4. Конфликт слияния
Оба меняют **одну и ту же строку** — заголовок README:
```bash
# A
git checkout develop && git pull && git checkout -b feature/TASK-11-readme-title-a
# в README.md замените первую строку на:  # TaskFlow CLI — менеджер задач
git commit -am "docs: изменить заголовок README (вариант A)" && git push -u origin HEAD
gh pr create --base develop --title "docs: заголовок README (A)" --body "Тест конфликта"
# B (из того же develop, до слияния PR A)
git checkout develop && git pull && git checkout -b feature/TASK-12-readme-title-b
# в README.md замените первую строку на:  # TaskFlow — консольный To-Do
git commit -am "docs: изменить заголовок README (вариант B)" && git push -u origin HEAD
gh pr create --base develop --title "docs: заголовок README (B)" --body "Тест конфликта"
```
Сольте PR A. У PR B появится «This branch has conflicts». Разрешение (B):
```bash
git fetch origin && git merge origin/develop        # конфликт в README.md
# в README.md увидите маркеры <<<<<<<  =======  >>>>>>>
# оставьте итоговую строку, напр.:  # TaskFlow CLI — консольный To-Do менеджер
git add README.md
git commit -m "fix: разрешить конфликт слияния в заголовке README"
git push
```
Затем Approve → Merge. **Сделайте скриншоты:** страницу конфликта, README с маркерами, итоговый merge.

## 5. Финал: develop → main
```bash
gh pr create --base main --head develop --title "release: спринт 1" --body "Итоги спринта"
```
После одобрения — Merge.

## 6. Что сфотографировать для отчёта
1. Доска Projects со спринтом · 2. Список issues · 3. Network graph (Insights → Network)
или `git log --oneline --graph --all` · 4. PR с комментарием ревью · 5. Страница конфликта · 6. Ссылка на репозиторий.
