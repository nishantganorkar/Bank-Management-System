import json
import random
import string
from pathlib import Path



class Bank:
    database = 'data.json'
    data = []

    try: 
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            print("No such file exist")

    except Exception as err:
        print(f"An exception occured as {err}")


    @classmethod
    def __update(cls):
        with open(cls.database,'w') as fs:
            fs.write(json.dumps(Bank.data))


    @classmethod
    def __accountgenerate(cls):
        num = random.choices(string.digits,k=10)
        id = num 
        random.shuffle(id)
        return "".join(id)



    def createaccount(self):
        info = {
            "name": input("Tell your Name :- "),
            "age": int(input("Tell your Age :- ")),
            "email": input("Tell your Email :- "),
            "pin": input("Tell your 4 number Pin :- "),
            "accountNo.": Bank.__accountgenerate(),
            "balance": 0 
        }
        if info['age'] < 18 or len(str(info['pin'])) != 4:
            print("Sorry you connot create your account")
        else:
            print("Account has been created successfully")
            for i in info:
                print(f"{i} : {info[i]}")
            print("Please note down your account number")

            Bank.data.append(info)

            Bank.__update()


    def depositmoney(self):
        accNumber = input("Please tell your account number :-")
        pin = input("Please tell your pin aswell :-")

        userdata = [i for i in Bank.data if i['accountNo.'] == accNumber and i['pin'] == pin]

        if not userdata:
            print("Sorry no data found")

        else:
            amount = int(input("How much you want to deposit :-"))
            if amount > 10000 or amount < 0:
                print("Sorry the Amount is too much you can deposite below 10,000 and above 0")

            else:
                userdata[0]['balance'] += amount
                Bank.__update()
                print("Amount deposited successfully")



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

