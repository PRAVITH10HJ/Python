# -*- coding: utf-8 -*-
"""
Created on Thu May  1 10:21:51 2025

@author: pravi
"""

import random
import mysql.connector
import os
import getpass

# Database connection (configurable for better portability)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'SQLPravith@10',
    'database': 'pravith',
    'charset': 'utf8'
}
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Pravith10")  # Set via environment variable for security

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def get_valid_date(prompt, year_range=(1980, 2003)):
    while True:
        try:
            date_str = input(prompt)
            year, month, day = map(int, date_str.split('-'))
            if not (1 <= month <= 12):
                raise ValueError("Invalid month.")
            if not (1 <= day <= 31):
                raise ValueError("Invalid day.")
            if not (year_range[0] <= year <= year_range[1]):
                raise ValueError("Year out of range.")
            return date_str
        except ValueError as e:
            print(f"Error: {e}")

def get_valid_input(prompt, valid_options):
    while True:
        value = input(prompt).strip().upper()
        if value in valid_options:
            return value
        print(f"Invalid input. Expected one of {valid_options}.")

def register_employee(cursor, connection):
    emp_id = random.randint(1000, 9999)
    print(f"Assigned Employee ID: {emp_id}")

    name = input("Enter Employee Name: ")
    gender = get_valid_input("Enter Gender (M/F/O): ", ["M", "F", "O"])
    dob = get_valid_date("Enter Date of Birth (YYYY-MM-DD): ")
    doj = get_valid_date("Enter Date of Joining (YYYY-MM-DD): ", (1980, 2025))

    designations = ["HR", "Manager", "Executive", "CEO", "President", "Vice President", "Accountant", "Clerk"]
    print("Available designations:", ", ".join(designations))
    des = input("Enter Designation (or 'NONE'): ").title()
    if des not in designations:
        des = "Intern"

    try:
        salary = int(input("Enter Basic Salary (or 000 for default): "))
        if salary == 0:
            salary = 10000
        elif salary < 10000:
            raise ValueError("Salary must be at least 10000.")
    except ValueError:
        salary = 10000

    address = input("Enter Address: ")

    query = """
        INSERT INTO Details_of_Employee
        (Employee_ID, Employee_name, Sex_of_Employee, Date_of_birth, Date_of_joinig,
         designation, Basic_salary, Employee_address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (emp_id, name, gender, dob, doj, des, salary, address)
    cursor.execute(query, values)
    connection.commit()
    print("Employee registered successfully.")

def search_employee(cursor):
    print("1. Search by Name\n2. Search by ID")
    choice = input("Choose an option: ")
    if choice == '1':
        name = input("Enter name: ")
        cursor.execute("SELECT * FROM Details_of_Employee WHERE Employee_name = %s", (name,))
    elif choice == '2':
        emp_id = input("Enter Employee ID: ")
        cursor.execute("SELECT * FROM Details_of_Employee WHERE Employee_ID = %s", (emp_id,))
    else:
        print("Invalid option.")
        return
    for row in cursor.fetchall():
        print(row)

def show_all_employees(cursor):
    cursor.execute("SELECT * FROM Details_of_Employee")
    for row in cursor.fetchall():
        print(row)

def delete_employee(cursor, connection):
    pw = getpass.getpass("Enter Admin Password: ")
    if pw != ADMIN_PASSWORD:
        print("Invalid password.")
        return
    emp_id = input("Enter Employee ID to delete: ")
    cursor.execute("DELETE FROM Details_of_Employee WHERE Employee_ID = %s", (emp_id,))
    connection.commit()
    print("Employee deleted.")

def delete_all_employees(cursor, connection):
    pw = getpass.getpass("Enter Admin Password: ")
    if pw != ADMIN_PASSWORD:
        print("Invalid password.")
        return
    cursor.execute("DROP TABLE IF EXISTS Details_of_Employee")
    connection.commit()
    print("All records deleted.")

def create_employee_table(cursor):
    pw = getpass.getpass("Enter Admin Password: ")
    if pw != ADMIN_PASSWORD:
        print("Invalid password.")
        return
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Details_of_Employee (
            Employee_ID VARCHAR(20) PRIMARY KEY,
            Employee_name VARCHAR(20) NOT NULL,
            Sex_of_Employee VARCHAR(10),
            Date_of_birth DATE NOT NULL,
            Date_of_joinig DATE NOT NULL,
            designation VARCHAR(20),
            Basic_salary INT DEFAULT 10000,
            Employee_address VARCHAR(100)
        )
    """)
    print("Employee table created.")

def main():
    connection = connect_db()
    cursor = connection.cursor()

    menu = """
    ================================================
    Sr No. | Options
    -----------------------------------------------
      0    | Exit this program
      1    | New employee registration
      2    | Search employee details
      3    | Show all employee records
      4    | Delete employee (Admin only)
      5    | Delete all records (Admin only)
      6    | Create employee table (Admin only)
    ================================================
    """
    while True:
        print(menu)
        choice = input("Enter your choice: ")

        if choice == '0':
            print("Exiting. Thank you!")
            break
        elif choice == '1':
            register_employee(cursor, connection)
        elif choice == '2':
            search_employee(cursor)
        elif choice == '3':
            show_all_employees(cursor)
        elif choice == '4':
            delete_employee(cursor, connection)
        elif choice == '5':
            delete_all_employees(cursor, connection)
        elif choice == '6':
            create_employee_table(cursor)
        else:
            print("Invalid choice. Please try again.")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
