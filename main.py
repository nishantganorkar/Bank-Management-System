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
        alpha = random.choices(string.ascii_letters,k=3)
        num = random.choices(string.digits,k=3)
        spchar = random.choices("!@#$%^&*",k=1)
        id = alpha + num + spchar
        random.shuffle(id)
        return "".join(id)



    def createaccount(self):
        info = {
            "name": input("Tell your Name :- "),
            "age": int(input("Tell your Age :- ")),
            "email": input("Tell your Email :- "),
            "pin": int(input("Tell your 4 number Pin :- ")),
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
