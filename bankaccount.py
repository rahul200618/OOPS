class bank:
    def __init__(self):
        self.account_no=0
        self.pincode=0
        self.balance=0
    def open_account(self,account_no,pincode,balance):
        self.account_no=account_no
        self.pincode=pincode
        self.balance=balance
        return "Account opened successfully"
    def check_balance(self,account_no,pincode,balance):
        if self.account_no==account_no:
            if self.pincode==pincode:
                return f"Your balance is {self.balance}" 
            else:
                return "Invalid pincode"
        else:
            return "Invalid account number"
    def deposit(self,account_no,pincode,amount):
        if self.account_no==account_no:
            if self.pincode==pincode:
                self.balance+=amount
                return f"Amount deposited successfully. New balance is {self.balance}"
            else:
                return "Invalid pincode"
        else:
            return "Invalid account number"
    def withdraw(self,account_no,pincode,amount):
        if self.account_no==account_no:
            if self.pincode==pincode:
                if self.balance>=amount:
                    self.balance-=amount
                    return f"Amount withdrawn successfully. New balance is {self.balance}"
                else:
                    return "Insufficient balance"
            else:
                return "Invalid pincode"
        else:
            return "Invalid account number"
if __name__=="__main__":
    my_bank_account = bank()

    print("Welcome to the Bank!")
    print("1. Open Account")
    print("2. Check Balance")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. Exit")

    while True:
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            acc_no = int(input("Enter account number: "))
            pin = int(input("Enter pincode: "))
            initial_balance = float(input("Enter initial balance: "))
            print(my_bank_account.open_account(acc_no, pin, initial_balance))
        elif choice == "2":
            acc_no = int(input("Enter account number: "))
            pin = int(input("Enter pincode: "))
            print(my_bank_account.check_balance(acc_no, pin, 0)) # Balance argument is not used in check_balance
        elif choice == "3":
            acc_no = int(input("Enter account number: "))
            pin = int(input("Enter pincode: "))
            amount = float(input("Enter amount to deposit: "))
            print(my_bank_account.deposit(acc_no, pin, amount))
        elif choice == "4":
            acc_no = int(input("Enter account number: "))
            pin = int(input("Enter pincode: "))
            amount = float(input("Enter amount to withdraw: "))
            print(my_bank_account.withdraw(acc_no, pin, amount))
        elif choice == "5":
            print("Thank you for banking with us!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")