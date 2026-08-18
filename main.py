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
        num = random.choices(string.digits,k=10)
        id = num 
        random.shuffle(id)
        return "".join(id)



    def createaccount(self):
        name = input("Tell your Name :- ")
        age = int(input("Tell your Age :- "))

        if age < 18:
            print("Sorry, you cannot create an account. Age must be 18 or above.")
            return

        email = input("Tell your Email :- ")
        pin = input("Tell your 4 number Pin :- ")

        if len(pin) != 4:
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

        amount = int(input("How much you want to deposit :- "))

        if amount > 10000 or amount <= 0:
            print("Sorry the amount should be between 1 and 10,000")
            return

        userdata[0]['balance'] += amount

        Bank.__update()

        print("Amount deposited successfully")
        print(f"Current Balance : {userdata[0]['balance']}")



    def withdrawtmoney(self):
            accNumber = input("Please tell your account number :-")
            pin = input("Please tell your pin aswell :-")
    
            userdata = [i for i in Bank.data if i['accountNo.'] == accNumber and i['pin'] == pin]
    
            if not userdata:
                print("Sorry no data found")
    
            else:
                amount = int(input("How much you want withdraw :-"))
                if userdata[0]['balance'] < amount:
                    print("Sorry you don't have that much money")
        
    
                else:
                    userdata[0]['balance'] -= amount
                    Bank.__update()
                    print("Amount withdrew successfully")



    def showdetails(self):
            accNumber = input("Please tell your account number :-")
            pin = input("Please tell your pin aswell :-")

            userdata = [i for i in Bank.data if i['accountNo.'] == accNumber and i['pin'] == pin]
            print("Your information are :\n")

            for i in userdata[0]:
                print(f"{i} : {userdata[0][i]}")



    def updatedetails(self):
            accNumber = input("Please tell your account number :-")
            pin = input("Please tell your pin aswell :-")
            
            userdata = [i for i in Bank.data if i['accountNo.'] == accNumber and i['pin'] == pin]

            if userdata == False:
                print("No such user found")

            else:
                print("\nYou cannot change the age, account number, and balance ")

                print("Fill the details for change or leave it empty if no change")

                newdata ={
                    "name": input("Please tell new name or press enter :- "),
                    "email": input("Please tell your new Email or press enter to skip :- "),
                    "pin": input("Enter new pin or press enter to skip :- ")
                }

                if newdata["name"] == "":
                    newdata["name"] = userdata[0]["name"]

                if newdata["email"] == "":
                    newdata["email"] = userdata[0]["email"]

                if newdata["pin"] == "":
                    newdata["pin"] = userdata[0]["pin"]

                newdata['age'] = userdata[0]['age']
                newdata['accountNo.'] = userdata[0]['accountNo.']
                newdata['balance'] = userdata[0]['balance']

                if type(newdata['pin']) == str:
                    newdata['pin'] == int(newdata['pin'])

                for i in newdata:
                    if newdata[i] == userdata[0][i]:
                        continue
                    else:
                        userdata[0][i] = newdata[i]

                Bank.__update()
                print("Details updates successfully")



    def delete(self):
            accNumber = input("Please tell your account number :-")
            pin = input("Please tell your pin aswell :-")
                        
            userdata = [i for i in Bank.data if i['accountNo.'] == accNumber and i['pin'] == pin]

            if userdata == False:
                print("Sorry no such data exist")
            else:
                check = input("Press Y if you actually want to delete the account or press N :-")
                if check == 'n' or check == 'N':
                    print("Bypassed")
                else:
                    index = Bank.data.index(userdata[0])
                    Bank.data.pop(index)
                    print("Account deleted successfully")
                    Bank.__update()


user = Bank()
print("Press 1 for Creating an Account")
print("Press 2 for Depositing the money in the bank")
print("Press 3 Withdrawing the money")
print("Press 4 for Details")
print("Press 5 for Updating the details")
print("Press 6 for Deleting your Account")

check = int(input("Tell your Response :- "))

if check == 1:
    user.createaccount()

if check == 2:
    user.depositmoney()

if check == 3:
    user.withdrawtmoney()

if check == 4:
    user.showdetails()

if check == 5:
    user.updatedetails()

if check == 6:
    user.delete()