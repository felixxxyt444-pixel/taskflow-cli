import argparse
from .todo import TaskManager, PRIORITIES

DB = "tasks.json"


def main() -> None:
    p = argparse.ArgumentParser(prog="taskflow", description="Консольный менеджер задач")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add"); a.add_argument("title")
    a.add_argument("--priority", choices=PRIORITIES, default="medium")
    a.add_argument("--deadline")
    l = sub.add_parser("list"); l.add_argument("--status", choices=["todo", "done"])
    d = sub.add_parser("done"); d.add_argument("id", type=int)
    r = sub.add_parser("delete"); r.add_argument("id", type=int)
    args = p.parse_args()

    m = TaskManager(); m.load(DB)
    try:
        if args.cmd == "add":
            t = m.add(args.title, args.priority, args.deadline); print(f"Добавлена задача #{t.id}")
        elif args.cmd == "list":
            for t in m.list(args.status):
                print(f"#{t.id} [{'x' if t.done else ' '}] {t.title} ({t.priority}) {t.deadline or ''}")
        elif args.cmd == "done":
            m.mark_done(args.id); print("Готово")
        elif args.cmd == "delete":
            m.delete(args.id); print("Удалено")
    except (KeyError, ValueError) as e:
        print(f"Ошибка: {e}")
    m.save(DB)


if __name__ == "__main__":
    main()
