import unittest
import os

from app.employee import Employee
from app.storage import save_employees, load_employees


class TestStorage(unittest.TestCase):

    TEST_FILE = "test_employees.json"

    def tearDown(self):
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

    def test_save_and_load(self):
        employees = [
            Employee(1, "Alice", "Engineering", 5000),
            Employee(2, "Bob", "HR", 4000)
        ]

        save_employees(self.TEST_FILE, employees)

        data = load_employees(self.TEST_FILE)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["name"], "Alice")


if __name__ == "__main__":
    unittest.main()