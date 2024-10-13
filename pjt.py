import json
import pandas as pd
from datetime import datetime
class User:
    def __init__(self, username, password):  
        self.username = username
        self.password = password
    @staticmethod
    def register():
        print(" User Registration")
        username = input("Enter a new username: ")
        password = input("Enter a new password: ")

        try:
            with open('users.json', 'r') as file:
                users = json.load(file)
        except FileNotFoundError:
            users = {}

        if username in users:
            print(" Username already exists. Please try again.")
            return None
        
        users[username] = password
        with open('users.json', 'w') as file:
            json.dump(users, file)
        
        print(f"User '{username}' registered successfully!")
        return User(username, password)
    @staticmethod
    def login():
        print("User Login")
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        try:
            with open('users.json', 'r') as file:
                users = json.load(file)
        except FileNotFoundError:
            print(" No users found. Please register first.")
            return None

        if username in users and users[username] == password:
            print(f" Login successful! Welcome, {username}.")
            return User(username, password)
        else:
            print("Invalid username or password. Please try again.")
            return None

    def logout(self):
        print(f"User '{self.username}' logged out successfully!")
        return None

class FinanceRec:
    def __init__(self, des, amt, category, date):
        self.des = des
        self.amt = amt
        self.category = category
        self.date = date
    def to_dict(self):
        return {
            "des": self.des,
            "amt": self.amt,
            "category": self.category,
            "date": self.date
        }

class FinanceManager:
    def __init__(self, user):
        self.user = user
        self.records = []
    def load_user(self):
        try:
            with open('finances.json', 'r') as file:
                data = json.load(file)
                self.records = [FinanceRec(**rec) for rec in data.get(self.user.username, [])]
        except FileNotFoundError:
            self.records = []
        except json.JSONDecodeError:
            print("Error loading data. Please try again.")
            self.records = []
    def save_data(self):
        try:
            with open('finances.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        except json.JSONDecodeError:
            print("Error loading data. Please try again.")
            data = {}
        data[self.user.username] = [rec.to_dict() for rec in self.records]

        with open('finances.json', 'w') as file:
            json.dump(data, file)
    def add_rec(self, rec):
        self.records.append(rec)
        self.save_data()

    def delete_rec(self, index):
        if 0 <= index < len(self.records):
            del self.records[index]
            self.save_data()
            print(" Record deleted successfully!")
        else:
            print(" Invalid record number.")


    def update_rec(self, index, new_rec):
        if 0 <= index < len(self.records):
            self.records[index] = new_rec
            self.save_data()
            print(" Record updated successfully!")
        else:
            print(" Invalid record number.")

    def generate_report(self):
        df = pd.DataFrame([rec.to_dict() for rec in self.records])
        if not df.empty:
            print(" Finance Report ")
            print(df.describe())
            print("---------")
        else:
            print(" No records available to generate a report.")

    def input_finance_record(self):
        print(" Add New Finance Record ")
        description = input("Enter the description: ")
        amount = float(input("Enter the amount: "))
        print("Select the category:")
        print("1. Income")
        print("2. Expense")
        choice = input("Enter your choice (1/2): ")
        
        if choice == '1':
            category = 'Income'
            amount = abs(amount)  
            print(" valid category selected.")

        elif choice == '2':
            category = 'Expense'
            amount = -abs(amount) 
            print(" valid category selected.")
 
        else:
            category = 'Unknown'
            print(" Invalid category selected.")
        date = datetime.now().strftime('%Y-%m-%d')

        return FinanceRec(description, amount, category, date)

    def display_rec(self):
        if not self.records:
            print(" No records available.")
            return
        print("Existing Records ")
        for idx, rec in enumerate(self.records):
            print(f"{idx + 1}. {rec.des} | {rec.amt} | {rec.category} | {rec.date}")
        print("----------")

    def total_income_expenses(self):
        df = pd.DataFrame([rec.to_dict() for rec in self.records])
        if not df.empty:
            total_income = df[df['category'].str.lower() == 'income']['amt'].sum()
            total_expenses = df[df['category'].str.lower() == 'expense']['amt'].sum()
            remaining_salary =total_income + total_expenses  
            
            print(f" Financial Overview ")
            print(f"Total Income: {total_income}")
            print(f"Total Expenses: {total_expenses}")
            print(f"Remaining Balance: {remaining_salary}")
        else:
            print(" No records available to calculate totals.")

    def spending_distribution(self):
        df = pd.DataFrame([rec.to_dict() for rec in self.records])
        if not df.empty:
            distribution = df.groupby('category')['amt'].sum().reset_index()
            print("Spending Distribution by Category ")
            print(distribution)
            print("---------")
        else:
            print("No records available to display distribution.")

    def monthly_trends(self):
        df = pd.DataFrame([rec.to_dict() for rec in self.records])
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df['month'] = df['date'].dt.to_period('M')
            trends = df.groupby(['month', 'category'])['amt'].sum().unstack(fill_value=0)
            print("Monthly Spending Trends")
            print(trends)
            print("-----------")
        else:
            print("No records available to display trends.")

def main():
    current_user = None

    while True:
        if not current_user:
            print("Welcome! Please Choose an Option:")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                current_user = User.register()
            elif choice == '2':
                current_user = User.login()
            elif choice == '3':
                print("See you next time.")
                break
            else:
                print(" Invalid choice.")

        else:
            print(f"{current_user.username}")
            print("1. Add Your Record")
            print("2. View Report")
            print("3. Delete Record")
            print("4. Update Record")
            print("5. Total Income and Expenses")
            print("6. Spending Distribution ")
            print("7. Spending Trends")
            print("8. Exit")
            choice = input("Enter your choice: ")
            finance_manager = FinanceManager(current_user)
            finance_manager.load_user()

            if choice == '1':
                rec = finance_manager.input_finance_record()
                if rec.category != 'Unknown':  
                    finance_manager.add_rec(rec)
                    print("Finance record added successfully")
            elif choice == '2':
                finance_manager.generate_report()
            elif choice == '3':
                finance_manager.display_rec()
                index = int(input("Enter record number to delete: ")) - 1
                finance_manager.delete_rec(index)
            elif choice == '4':
                finance_manager.display_rec()
                index = int(input("Enter record number to update: ")) - 1
                new_rec = finance_manager.input_finance_rec()
                finance_manager.update_rec(index, new_rec)
            elif choice == '5':
                finance_manager.total_income_expenses()
            elif choice == '6':
                finance_manager.spending_distribution()
            elif choice == '7':
                finance_manager.monthly_trends()
            elif choice == '8':
                current_user.logout() 
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    main()