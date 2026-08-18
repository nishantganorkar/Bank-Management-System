import json
import random
import string
from pathlib import Path


class Bank:
    database = Path(__file__).parent / 'data.json'
    data = []

    try:
        if database.exists():
            with open(database) as fs:
                data = json.load(fs)
        else:
            print("No such file exists")

    except Exception as err:
        print(f"An exception occurred as {err}")

    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            json.dump(cls.data, fs, indent=4)

        print("Data saved successfully!")

    @classmethod
    def __accountgenerate(cls):
        while True:
            account = ''.join(random.choices(string.digits, k=10))

            if not any(i['accountNo.'] == account for i in cls.data):
                return account

    def createaccount(self):
        name = input("Tell your Name :- ")

        try:
            age = int(input("Tell your Age :- "))
        except ValueError:
            print("Please enter a valid age.")
            return

        if age < 18:
            print("Sorry, you cannot create an account. Age must be 18 or above.")
            return

        email = input("Tell your Email :- ")
        pin = input("Tell your 4 number Pin :- ")

        if len(pin) != 4 or not pin.isdigit():
            print("Sorry, PIN must be exactly 4 digits.")
            return

        info = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "accountNo.": Bank.__accountgenerate(),
            "balance": 0
        }

        print("Account has been created successfully")

        for i in info:
            print(f"{i} : {info[i]}")

        print("Please note down your account number")

        Bank.data.append(info)
        Bank.__update()

    def depositmoney(self):
        accNumber = input("Please tell your account number :- ")
        pin = input("Please tell your pin aswell :- ")

        userdata = [
            i for i in Bank.data
            if i['accountNo.'] == accNumber and i['pin'] == pin
        ]

        if not userdata:
            print("Sorry no data found")
            return

        try:
            amount = int(input("How much you want to deposit :- "))
        except ValueError:
            print("Please enter a valid amount.")
            return

        if amount > 10000 or amount <= 0:
            print("Sorry the amount should be between 1 and 10,000")
            return

        userdata[0]['balance'] += amount

        Bank.__update()

        print("Amount deposited successfully")
        print(f"Current Balance : {userdata[0]['balance']}")

    def withdrawtmoney(self):
        accNumber = input("Please tell your account number :- ")
        pin = input("Please tell your pin aswell :- ")

        userdata = [
            i for i in Bank.data
            if i['accountNo.'] == accNumber and i['pin'] == pin
        ]

        if not userdata:
            print("Sorry no data found")
            return

        try:
            amount = int(input("How much you want withdraw :- "))
        except ValueError:
            print("Please enter a valid amount.")
            return

        if amount <= 0:
            print("Withdrawal amount must be greater than 0.")
            return

        if amount > 10000:
            print("Maximum withdrawal amount is 10,000.")
            return

        if userdata[0]['balance'] < amount:
            print("Sorry you don't have that much money")
            return

        userdata[0]['balance'] -= amount

        Bank.__update()

        print("Amount withdrew successfully")
        print(f"Current Balance : {userdata[0]['balance']}")

    def showdetails(self):
        accNumber = input("Please tell your account number :- ")
        pin = input("Please tell your pin aswell :- ")

        userdata = [
            i for i in Bank.data
            if i['accountNo.'] == accNumber and i['pin'] == pin
        ]

        if not userdata:
            print("Sorry no data found")
            return

        print("Your information are :\n")

        for i in userdata[0]:
            print(f"{i} : {userdata[0][i]}")

    def updatedetails(self):
        accNumber = input("Please tell your account number :- ")
        pin = input("Please tell your pin aswell :- ")

        userdata = [
            i for i in Bank.data
            if i['accountNo.'] == accNumber and i['pin'] == pin
        ]

        if not userdata:
            print("No such user found")
            return

        print("\nYou cannot change the age, account number, and balance")

        print("Fill the details for change or leave it empty if no change")

        newdata = {
            "name": input("Please tell new name or press enter to skip :- "),
            "email": input("Please tell your new Email or press enter to skip :- "),
            "pin": input("Enter new pin or press enter to skip :- ")
        }

        if newdata["name"] == "":
            newdata["name"] = userdata[0]["name"]

        if newdata["email"] == "":
            newdata["email"] = userdata[0]["email"]

        if newdata["pin"] == "":
            newdata["pin"] = userdata[0]["pin"]

        if newdata["pin"] != "":
            if len(newdata["pin"]) != 4 or not newdata["pin"].isdigit():
                print("PIN must be exactly 4 digits.")
                return

        newdata['age'] = userdata[0]['age']
        newdata['accountNo.'] = userdata[0]['accountNo.']
        newdata['balance'] = userdata[0]['balance']

        for i in newdata:
            if newdata[i] == userdata[0][i]:
                continue
            else:
                userdata[0][i] = newdata[i]

        Bank.__update()

        print("Details updated successfully")

    def delete(self):
        accNumber = input("Please tell your account number :- ")
        pin = input("Please tell your pin aswell :- ")

        userdata = [
            i for i in Bank.data
            if i['accountNo.'] == accNumber and i['pin'] == pin
        ]

        if not userdata:
            print("Sorry no such data exist")
            return

        check = input(
            "Press Y if you actually want to delete the account or press N :- "
        )

        if check == 'n' or check == 'N':
            print("Bypassed")
        elif check == 'y' or check == 'Y':
            index = Bank.data.index(userdata[0])
            Bank.data.pop(index)

            print("Account deleted successfully")

            Bank.__update()
        else:
            print("Invalid choice")


user = Bank()

while True:

    print("\n===== BANK MANAGEMENT SYSTEM =====")
    print("Press 1 for Creating an Account")
    print("Press 2 for Depositing the money in the bank")
    print("Press 3 for Withdrawing the money")
    print("Press 4 for Details")
    print("Press 5 for Updating the details")
    print("Press 6 for Deleting your Account")
    print("Press 7 for Exit")

    try:
        check = int(input("Tell your Response :- "))
    except ValueError:
        print("Please enter a valid number.")
        continue

    if check == 1:
        user.createaccount()

    elif check == 2:
        user.depositmoney()

    elif check == 3:
        user.withdrawtmoney()

    elif check == 4:
        user.showdetails()

    elif check == 5:
        user.updatedetails()

    elif check == 6:
        user.delete()

    elif check == 7:
        print("Thank you for using Bank Management System!")
        break

    else:
        print("Invalid choice. Please try again.")