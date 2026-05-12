import logging

logging.basicConfig(level=logging.INFO)


def calculate_average_salary(employee_data):
    if not employee_data:
        return 0

    total = sum(emp["salary"] for emp in employee_data)
    return total / len(employee_data)


def department_filter(employee_data, department):
    return [
        emp for emp in employee_data
        if emp["department"].lower() == department.lower()
    ]