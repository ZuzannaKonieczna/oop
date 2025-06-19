class Person:
    def __init__(self, name , age):
        self.name = name
        self.age = age
        self.gift_list = []
    def add_gift(self, prezent):
        self.gift_list.append(prezent)
    def pokaz_prezenty(self):
        print(f"\nPrezenty dla {self.imie}:")
        if not self.lista_prezentow:
            print("Brak prezentów")
            return
        for i, p in enumerate(self.lista_prezentow, 1):
            print(f"{i}. {p.nazwa} (od {p.nadawca.imie}) - {p.cena} zł")
           
    
class Gift:
    def __init__(self, name, price, name_Giver):
        self.name = name
        self.price = price
        self.giftGiver = name_Giver
    def add_giftGiver(self, name):
        self.giftGiver.append(name)

zuzia = Person("Zuzia", 18)

print(zuzia.age)

x = input("What gift do you want to give: ")
zuzia.add_gift(x)
zuzia.pokaz_prezenty()