import unittest
from app.utils import calculate_average_salary, department_filter


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.data = [
            {"name": "Alice", "department": "Engineering", "salary": 5000},
            {"name": "Bob", "department": "HR", "salary": 4000},
            {"name": "Charlie", "department": "Engineering", "salary": 6000},
        ]

    def test_average_salary(self):
        avg = calculate_average_salary(self.data)
        self.assertEqual(avg, 5000)

    def test_department_filter(self):
        result = department_filter(self.data, "Engineering")
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()