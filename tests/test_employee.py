import unittest
from app.employee import Employee


class TestEmployee(unittest.TestCase):

    def test_yearly_salary(self):
        emp = Employee(1, "Alice", "Engineering", 5000)
        self.assertEqual(emp.yearly_salary(), 60000)

    def test_to_dict(self):
        emp = Employee(2, "Bob", "HR", 4000)

        expected = {
            "emp_id": 2,
            "name": "Bob",
            "department": "HR",
            "salary": 4000
        }

        self.assertEqual(emp.to_dict(), expected)


if __name__ == "__main__":
    unittest.main()