import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")

        self.create_widgets()
        self.setup_database()
        self.root.protocol("WM_DELETE_WINDOW", self.close_connection)

    def create_widgets(self):
        def add_label_entry(row, text):
            tk.Label(self.root, text=text).grid(row=row, column=0, padx=10, pady=10)
            entry = tk.Entry(self.root)
            entry.grid(row=row, column=1, padx=10, pady=10)
            return entry

        self.name_entry = add_label_entry(0, "Name")
        self.height_entry = add_label_entry(1, "Height (cm)")
        self.weight_entry = add_label_entry(2, "Weight (kg)")
        self.calculate_button = tk.Button(self.root, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.grid(row=3, column=0, columnspan=2, pady=10)
        self.view_history_button = tk.Button(self.root, text="View History", command=self.view_history)
        self.view_history_button.grid(row=4, column=0, columnspan=2, pady=10)

    def setup_database(self):
        self.conn = sqlite3.connect('bmi_data.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY,name TEXT,
                height REAL,
                weight REAL,
                bmi REAL,
                category TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def calculate_bmi(self):
        try:
            name = self.name_entry.get()
            height = float(self.height_entry.get()) / 100
            weight = float(self.weight_entry.get())

            if not name or height <= 0 or weight <= 0:
                raise ValueError("Invalid input values")

            bmi = weight / (height ** 2)
            category = self.categorize_bmi(bmi)

            self.cursor.execute('''
                INSERT INTO bmi_records (name, height, weight, bmi, category)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, height, weight, bmi, category))
            self.conn.commit()

            messagebox.showinfo("BMI Result", f"BMI: {bmi:.2f}\nCategory: {category}")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numerical values for height and weight.")

    def categorize_bmi(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    def view_history(self):
        self.cursor.execute('SELECT * FROM bmi_records')
        records = self.cursor.fetchall()
        if not records:
            messagebox.showinfo("History", "No records found.")
            return

        names = [record[1] for record in records]
        bmis = [record[4] for record in records]

        plt.clf()
        plt.bar(names, bmis, color='blue')
        plt.xlabel('Names')
        plt.ylabel('BMI')
        plt.title('BMI History')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def close_connection(self):
        self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()
