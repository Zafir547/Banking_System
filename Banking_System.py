import json
from datetime import datetime


def load_accounts(filename='accounts.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_accounts(accounts, filename='accounts.json'):
    with open(filename, 'w') as file:
        json.dump(accounts, file, indent=4)

def create_account(name, initial_balance=0.0):
    accounts = load_accounts()
    if name in accounts:
        print(f"Account for {name} already exists.")
        return accounts[name]
    account = {
        "name": name,
        "balance": initial_balance,
        "transactions": []
    }
    accounts[name] = account
    save_accounts(accounts)
    print(f"Account for {name} created with balance ${initial_balance:.2f}.")
    return account

def deposit(account, amount):
    if amount <= 0:
        print("Deposit amount must be positive.")
        return account
    account['balance'] += amount
    transaction = {
        "type": "Deposit",
        "amount": amount,
        "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    account['transactions'].append(transaction)
    accounts = load_accounts()
    accounts[account['name']] = account
    save_accounts(accounts)
    print(f"{account['name']} deposited ${amount:.2f}. New balance: ${account['balance']:.2f}.")
    return account

def withdraw(account, amount):
    if amount <= 0:
        print("Withdrawal amount must be positive.")
        return account
    if account['balance'] < amount:
        print("Insufficient balance.")
        return account
    account['balance'] -= amount
    transaction = {
        "type": "Withdrawal",
        "amount": amount,
        "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    account['transactions'].append(transaction)
    accounts = load_accounts()
    accounts[account['name']] = account
    save_accounts(accounts)
    print(f"{account['name']} withdrew  ${amount:.2f}. New balance: ${account['balance']:.2f}.")
    return account

def check_balance(account):
    print(f"{account['name']}'s current balance: ${account['balance']:.2f}")
    return account['balance']

def print_statement(account):
    print(f"Account statement for {account['name']}:")
    balance = 0.0
    for transaction in account['transactions']:
        if transaction['type'] == 'Deposit':
            balance += transaction['amount']
        elif transaction['type'] == 'Withdrawal':
            balance -= transaction['amount']
        print(f"- {transaction['type']}: ${transaction['amount']:.2f}. New Balance: ${balance:.2f}")

def main():
    accounts = load_accounts()
    while True:
        print("\nBanking System Menu:")
        print("1. Create an Account")
        print("2. Deposit Money")
        print("3. Withdaw Money")
        print("4. Check Balance")
        print("5. Print Statement")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            name = input("Enter account holder's name: ")
            initial_balance = float(input("Enter initial balance: "))
            accounts[name] = create_account(name, initial_balance)
        elif choice == '2':
            name = input("Enter account holder's name: ")
            if name in accounts:
                amount = float(input("Enter amount to deposit: "))
                accounts[name] = deposit(accounts[name], amount)
            else:
                print("Account not found.")
        elif choice == '3':
            name = input("Enter account holder's name: ")
            if name in accounts:
                amount = float(input("Enter amount to withdraw: "))
                accounts[name] = withdraw(accounts[name], amount)
            else:
                print("Account not found.")
        elif choice == '4':
            name = input("Enter account holder's name: ")
            if name in accounts:
                check_balance(accounts[name])
            else:
                print("Account not found.")
        elif choice == '5':
            name = input("Enter account holder's name: ")
            if name in accounts:
                print_statement(accounts[name])
            else:
                print("Account not found.")
        elif choice == '6':
            print("Existing the banking system.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
