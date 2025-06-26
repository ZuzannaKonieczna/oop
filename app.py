import json
from datetime import datetime

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.gift_list = []
    
    def add_gift(self, gift):
        self.gift_list.append(gift)
    
    def show_gifts(self):
        print(f"\nGifts for {self.name}:")
        if not self.gift_list:
            print("No gifts")
            return
        for i, g in enumerate(self.gift_list, 1):
            print(f"{i}. {g.name} (from {g.giver.name}) - {g.price} PLN")
    
    def __str__(self):
        return f"{self.name} ({self.age} years old)"

class Gift:
    def __init__(self, name, price, giver, recipient):
        self.name = name
        self.price = price
        self.giver = giver
        self.recipient = recipient
    
    def show_info(self):
        print(f"\nGift: {self.name}")
        print(f"Price: {self.price} PLN")
        print(f"From: {self.giver.name}")
        print(f"To: {self.recipient.name}")

