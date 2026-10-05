import random
from datetime import datetime
import json
import os


DATA_FILE = "accounts.json"


# ---------------- LOAD DATA ----------------

def load_accounts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}


# ---------------- SAVE DATA ----------------

def save_accounts(accounts):
    with open(DATA_FILE, "w") as file:
        json.dump(accounts, file, indent=4)


# ---------------- GENERATE ACCOUNT NUMBER ----------------

def generate_account_number(accounts):
    while True:
        account_number = str(random.randint(1000000000, 9999999999))

        if account_number not in accounts:
            return account_number


# ---------------- CREATE ACCOUNT ----------------

def create_account(accounts):

    print("\n========== CREATE ACCOUNT ==========")

    name = input("Enter your name: ")
    phone = input("Enter phone number: ")

    while True:
        pin = input("Create 4-digit PIN: ")

        if len(pin) == 4 and pin.isdigit():
            break
        else:
            print("PIN must contain exactly 4 digits.")

    account_number = generate_account_number(accounts)

    accounts[account_number] = {
        "name": name,
        "phone": phone,
        "pin": pin,
        "balance": 0,
        "transactions": []
    }

    save_accounts(accounts)

    print("\nAccount created successfully!")
    print("Your Account Number is:", account_number)
    print("Please remember your account number and PIN.")


# ---------------- LOGIN ----------------

def login(accounts):

    print("\n========== LOGIN ==========")

    account_number = input("Enter Account Number: ")
    pin = input("Enter PIN: ")

    if account_number in accounts:

        if accounts[account_number]["pin"] == pin:
            print("\nLogin successful!")
            print("Welcome,", accounts[account_number]["name"])

            account_menu(accounts, account_number)
        else:
            print("Incorrect PIN.")

    else:
        print("Account not found.")


# ---------------- CHECK BALANCE ----------------

def check_balance(account):

    print("\n========== CHECK BALANCE ==========")
    print("Current Balance: ₹", account["balance"])


# ---------------- DEPOSIT ----------------

def deposit(account):

    print("\n========== DEPOSIT MONEY ==========")

    try:
        amount = float(input("Enter amount to deposit: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        account["balance"] += amount

        transaction = {
            "type": "Deposit",
            "amount": amount,
            "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }

        account["transactions"].append(transaction)

        print("₹", amount, "deposited successfully.")
        print("New Balance: ₹", account["balance"])

    except ValueError:
        print("Please enter a valid amount.")


# ---------------- WITHDRAW ----------------

def withdraw(account):

    print("\n========== WITHDRAW MONEY ==========")

    try:
        amount = float(input("Enter amount to withdraw: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        if amount > account["balance"]:
            print("Insufficient balance.")
            return

        account["balance"] -= amount

        transaction = {
            "type": "Withdrawal",
            "amount": amount,
            "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }

        account["transactions"].append(transaction)

        print("₹", amount, "withdrawn successfully.")
        print("Remaining Balance: ₹", account["balance"])

    except ValueError:
        print("Please enter a valid amount.")


# ---------------- TRANSFER ----------------

def transfer(accounts, sender_account_number):

    print("\n========== TRANSFER MONEY ==========")

    receiver_account_number = input(
        "Enter receiver account number: "
    )

    if receiver_account_number not in accounts:
        print("Receiver account does not exist.")
        return

    if receiver_account_number == sender_account_number:
        print("You cannot transfer money to your own account.")
        return

    try:
        amount = float(input("Enter amount to transfer: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        sender = accounts[sender_account_number]
        receiver = accounts[receiver_account_number]

        if amount > sender["balance"]:
            print("Insufficient balance.")
            return

        sender["balance"] -= amount
        receiver["balance"] += amount

        current_time = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        sender_transaction = {
            "type": "Transfer Sent",
            "amount": amount,
            "to": receiver_account_number,
            "date": current_time
        }

        receiver_transaction = {
            "type": "Transfer Received",
            "amount": amount,
            "from": sender_account_number,
            "date": current_time
        }

        sender["transactions"].append(sender_transaction)
        receiver["transactions"].append(receiver_transaction)

        print("₹", amount, "transferred successfully.")

    except ValueError:
        print("Please enter a valid amount.")


# ---------------- TRANSACTION HISTORY ----------------

def transaction_history(account):

    print("\n========== TRANSACTION HISTORY ==========")

    transactions = account["transactions"]

    if len(transactions) == 0:
        print("No transactions available.")
        return

    for i, transaction in enumerate(transactions, start=1):

        print("\nTransaction", i)

        print("Type:", transaction["type"])
        print("Amount: ₹", transaction["amount"])

        if "to" in transaction:
            print("To Account:", transaction["to"])

        if "from" in transaction:
            print("From Account:", transaction["from"])

        print("Date:", transaction["date"])


# ---------------- CHANGE PIN ----------------

def change_pin(account):

    print("\n========== CHANGE PIN ==========")

    old_pin = input("Enter old PIN: ")

    if old_pin != account["pin"]:
        print("Incorrect old PIN.")
        return

    while True:

        new_pin = input("Enter new 4-digit PIN: ")

        if len(new_pin) == 4 and new_pin.isdigit():
            break

        print("PIN must contain exactly 4 digits.")

    confirm_pin = input("Confirm new PIN: ")

    if new_pin != confirm_pin:
        print("PINs do not match.")
        return

    account["pin"] = new_pin

    print("PIN changed successfully.")


# ---------------- ACCOUNT MENU ----------------

def account_menu(accounts, account_number):

    while True:

        print("\n")
        print("======================================")
        print("             ACCOUNT MENU")
        print("======================================")

        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Transaction History")
        print("6. Change PIN")
        print("7. Logout")

        print("======================================")

        choice = input("Enter your choice: ")

        account = accounts[account_number]

        if choice == "1":
            check_balance(account)

        elif choice == "2":
            deposit(account)
            save_accounts(accounts)

        elif choice == "3":
            withdraw(account)
            save_accounts(accounts)

        elif choice == "4":
            transfer(accounts, account_number)
            save_accounts(accounts)

        elif choice == "5":
            transaction_history(account)

        elif choice == "6":
            change_pin(account)
            save_accounts(accounts)

        elif choice == "7":
            print("\nLogged out successfully.")
            print("Returning to Main Menu...")
            break

        else:
            print("Invalid choice. Please try again.")


# ---------------- MAIN MENU ----------------

def main():

    accounts = load_accounts()

    while True:

        print("\n")
        print("======================================")
        print("        BANKING SYSTEM")
        print("======================================")

        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        print("======================================")

        choice = input("Enter your choice: ")

        if choice == "1":

            create_account(accounts)

        elif choice == "2":

            login(accounts)

        elif choice == "3":

            print("\nThank you for using Banking System.")
            break

        else:

            print("Invalid choice. Please try again.")


# ---------------- PROGRAM START ----------------

if __name__ == "__main__":
    main()