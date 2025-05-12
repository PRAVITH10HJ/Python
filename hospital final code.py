# -*- coding: utf-8 -*-
"""
Created on Wed May  7 12:57:36 2025

@author: pravi
"""
# -*- coding: utf-8 -*-
"""
Expanded Hospital Management System (DBMS Project)
Author: Pravith
"""

import random
import mysql.connector
import os
import getpass

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'SQLPravith@10',
    'database': 'pravith',
    'charset': 'utf8'
}

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Pravith10")

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def get_valid_date(prompt, year_range=(1920, 2025)):
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

# ==================== PATIENT ====================

def create_patients_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Patients (
            patient_id INT PRIMARY KEY,
            name VARCHAR(50),
            gender VARCHAR(10),
            dob DATE,
            phone VARCHAR(15),
            address VARCHAR(100),
            blood_type VARCHAR(5),
            date_registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Patients table created.")

def register_patient(cursor, connection):
    pid = random.randint(1000, 9999)
    print(f"Assigned Patient ID: {pid}")
    name = input("Enter Patient Name: ")
    gender = get_valid_input("Gender (M/F/O): ", ["M", "F", "O"])
    dob = get_valid_date("Date of Birth (YYYY-MM-DD): ")
    phone = input("Phone: ")
    address = input("Address: ")
    blood_type = input("Blood Type: ").upper()
    cursor.execute("""
        INSERT INTO Patients (patient_id, name, gender, dob, phone, address, blood_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (pid, name, gender, dob, phone, address, blood_type))
    connection.commit()
    print("✅ Patient registered.")

def view_patients(cursor):
    cursor.execute("SELECT * FROM Patients")
    for row in cursor.fetchall():
        print(row)

# ==================== DOCTOR ====================

def create_doctors_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Doctors (
            doctor_id INT PRIMARY KEY,
            name VARCHAR(50),
            specialty VARCHAR(50),
            phone VARCHAR(15),
            email VARCHAR(100),
            room_number VARCHAR(10),
            date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Doctors table created.")

def register_doctor(cursor, connection):
    did = random.randint(5000, 9999)
    print(f"Assigned Doctor ID: {did}")
    name = input("Enter Doctor Name: ")
    specialty = input("Specialty: ")
    phone = input("Phone: ")
    email = input("Email: ")
    room = input("Room Number: ")
    cursor.execute("""
        INSERT INTO Doctors (doctor_id, name, specialty, phone, email, room_number)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (did, name, specialty, phone, email, room))
    connection.commit()
    print("✅ Doctor registered.")

def view_doctors(cursor):
    cursor.execute("SELECT * FROM Doctors")
    for row in cursor.fetchall():
        print(row)

# ==================== APPOINTMENT ====================

def create_appointments_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Appointments (
            appointment_id INT PRIMARY KEY AUTO_INCREMENT,
            patient_id INT,
            doctor_id INT,
            appointment_date DATETIME,
            status VARCHAR(20),
            reason TEXT,
            FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
            FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
        )
    """)
    print("✅ Appointments table created.")

def book_appointment(cursor, connection):
    pid = input("Enter Patient ID: ")
    did = input("Enter Doctor ID: ")
    date = input("Enter Appointment Date and Time (YYYY-MM-DD HH:MM:SS): ")
    reason = input("Reason for Visit: ")
    cursor.execute("""
        INSERT INTO Appointments (patient_id, doctor_id, appointment_date, status, reason)
        VALUES (%s, %s, %s, 'Scheduled', %s)
    """, (pid, did, date, reason))
    connection.commit()
    print("✅ Appointment booked.")

def view_appointments(cursor):
    cursor.execute("SELECT * FROM Appointments")
    for row in cursor.fetchall():
        print(row)

# ==================== BILL ====================

def create_bills_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Bills (
            bill_id INT PRIMARY KEY AUTO_INCREMENT,
            patient_id INT,
            total_amount DECIMAL(10, 2),
            status VARCHAR(20),
            bill_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
        )
    """)
    print("✅ Bills table created.")

def generate_bill(cursor, connection):
    pid = input("Enter Patient ID: ")
    amount = float(input("Enter Total Amount: "))
    status = input("Status (Paid/Unpaid): ")
    cursor.execute("""
        INSERT INTO Bills (patient_id, total_amount, status)
        VALUES (%s, %s, %s)
    """, (pid, amount, status))
    connection.commit()
    print("✅ Bill generated.")

def view_bills(cursor):
    cursor.execute("SELECT * FROM Bills")
    for row in cursor.fetchall():
        print(row)

# ==================== MEDICAL HISTORY ====================

def create_history_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Medical_History (
            history_id INT PRIMARY KEY AUTO_INCREMENT,
            patient_id INT,
            doctor_id INT,
            diagnosis TEXT,
            treatment TEXT,
            prescription TEXT,
            visit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
            FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
        )
    """)
    print("✅ Medical history table created.")

def add_history(cursor, connection):
    pid = input("Enter Patient ID: ")
    did = input("Enter Doctor ID: ")
    diagnosis = input("Diagnosis: ")
    treatment = input("Treatment: ")
    prescription = input("Prescription: ")
    cursor.execute("""
        INSERT INTO Medical_History (patient_id, doctor_id, diagnosis, treatment, prescription)
        VALUES (%s, %s, %s, %s, %s)
    """, (pid, did, diagnosis, treatment, prescription))
    connection.commit()
    print("✅ Medical history recorded.")

def view_history(cursor):
    cursor.execute("SELECT * FROM Medical_History")
    for row in cursor.fetchall():
        print(row)

# ==================== NEW FUNCTION: SELECT PATIENT OR DOCTOR ====================

def select_patient_or_doctor(cursor):
    print("\nSelect Record Type:")
    print("1. Select Patient")
    print("2. Select Doctor (Password Required)")
    choice = input("Enter your choice (1/2): ")

    if choice == '1':
        pid = input("Enter Patient ID: ")
        cursor.execute("SELECT * FROM Patients WHERE patient_id = %s", (pid,))
        result = cursor.fetchone()
        if result:
            print("✅ Patient Found:", result)
        else:
            print("❌ No patient found with that ID.")
    
    elif choice == '2':
        password = getpass.getpass("Enter Doctor Access Password: ")
        if password == ADMIN_PASSWORD:
            did = input("Enter Doctor ID: ")
            cursor.execute("SELECT * FROM Doctors WHERE doctor_id = %s", (did,))
            result = cursor.fetchone()
            if result:
                print("✅ Doctor Found:", result)
            else:
                print("❌ No doctor found with that ID.")
        else:
            print("❌ Incorrect password.")
    
    else:
        print("❌ Invalid selection.")

# ==================== MAIN MENU ====================

def main():
    conn = connect_db()
    cur = conn.cursor()

    menu = """
=============== Hospital Management System ===============
1. Register Patient
2. Register Doctor
3. Book Appointment
4. Generate Bill
5. Add Medical History
6. View Patients
7. View Doctors
8. View Appointments
9. View Bills
10. View Medical History
11. Create All Tables (Admin)
12. Select Patient or Doctor (Secure Access)
0. Exit
===========================================================
"""

    while True:
        print(menu)
        choice = input("Enter your choice: ")
        if choice == '1':
            register_patient(cur, conn)
        elif choice == '2':
            register_doctor(cur, conn)
        elif choice == '3':
            book_appointment(cur, conn)
        elif choice == '4':
            generate_bill(cur, conn)
        elif choice == '5':
            add_history(cur, conn)
        elif choice == '6':
            view_patients(cur)
        elif choice == '7':
            view_doctors(cur)
        elif choice == '8':
            view_appointments(cur)
        elif choice == '9':
            view_bills(cur)
        elif choice == '10':
            view_history(cur)
        elif choice == '11':
            pw = getpass.getpass("Enter Admin Password: ")
            if pw == ADMIN_PASSWORD:
                create_patients_table(cur)
                create_doctors_table(cur)
                create_appointments_table(cur)
                create_bills_table(cur)
                create_history_table(cur)
            else:
                print("❌ Incorrect password.")
        elif choice == '12':
            select_patient_or_doctor(cur)
        elif choice == '0':
            print("👋 Exiting system. Thank you.")
            break
        else:
            print("❌ Invalid choice.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
