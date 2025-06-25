class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age 
        self.gift_list = []
    
class Gifts:
    def __init__(self, name, gift_giver, ):
        self.name = name 
        self.gift_giver = gift_giver
    

zuzia = Person("Zuzia", 18)
phone = Gifts("Phone", "Zuzia")

print("Name: ", zuzia.name, " Age: ", zuzia.age, "she/he buys: ", phone.name )