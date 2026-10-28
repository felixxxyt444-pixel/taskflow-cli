import os, tempfile, unittest
from taskflow.todo import TaskManager


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        self.m = TaskManager()

    def test_add_and_list(self):
        self.m.add("Сдать отчёт")
        self.assertEqual(len(self.m.list()), 1)

    def test_empty_title_rejected(self):
        with self.assertRaises(ValueError):
            self.m.add("   ")

    def test_mark_done_and_filter(self):
        t = self.m.add("A"); self.m.add("B")
        self.m.mark_done(t.id)
        self.assertEqual([x.title for x in self.m.list("done")], ["A"])
        self.assertEqual([x.title for x in self.m.list("todo")], ["B"])

    def test_delete(self):
        t = self.m.add("A"); self.m.delete(t.id)
        self.assertEqual(self.m.list(), [])
        with self.assertRaises(KeyError):
            self.m.delete(t.id)

    def test_save_load(self):
        self.m.add("A", "high", "2026-11-01")
        path = os.path.join(tempfile.mkdtemp(), "t.json")
        self.m.save(path)
        m2 = TaskManager(); m2.load(path)
        self.assertEqual(m2.list()[0].priority, "high")
        self.assertEqual(m2.add("B").id, 2)


if __name__ == "__main__":
    unittest.main()
