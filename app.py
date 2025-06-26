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

class Task:
    def __init__(self, description, deadline, responsible_person):
        self.description = description
        self.deadline = deadline
        self.responsible_person = responsible_person
        self.status = "Not done"
    
    def mark_as_done(self):
        self.status = "Done"
        print(f"Task '{self.description}' has been marked as done.")
    
    def __str__(self):
        return f"{self.description} (deadline: {self.deadline}, responsible: {self.responsible_person.name}, status: {self.status})"

class BirthdayParty:
    def __init__(self, celebrant, date, location, budget):
        self.celebrant = celebrant
        self.date = date
        self.location = location
        self.budget = budget
        self.guest_list = []
        self.task_list = []
    
    def add_guest(self, guest):
        if guest not in self.guest_list:
            self.guest_list.append(guest)
            print(f"Added guest: {guest.name}")
        else:
            print(f"{guest.name} is already on the guest list")
    
    def remove_guest(self, guest):
        if guest in self.guest_list:
            self.guest_list.remove(guest)
            print(f"Removed guest: {guest.name}")
        else:
            print(f"{guest.name} was not on the guest list")
    
    def schedule_task(self, task):
        self.task_list.append(task)
        print(f"Added task: {task.description}")
    
    def show_tasks(self):
        print("\nTask list:")
        if not self.task_list:
            print("No tasks")
            return
        for i, t in enumerate(self.task_list, 1):
            print(f"{i}. {t}")
    
    def show_guests(self):
        print("\nGuest list:")
        if not self.guest_list:
            print("No guests")
            return
        for i, g in enumerate(self.guest_list, 1):
            print(f"{i}. {g}")
    
    def calculate_gifts_cost(self):
        total = sum(g.price for guest in self.guest_list for g in guest.gift_list)
        print(f"\nTotal value of gifts: {total} PLN")
        return total
    
    def show_summary(self):
        print("\n=== PARTY SUMMARY ===")
        print(f"Celebrant: {self.celebrant}")
        print(f"Date: {self.date}")
        print(f"Location: {self.location}")
        print(f"Budget: {self.budget} PLN")
        
        self.show_guests()
        self.show_tasks()
        
        gifts_total = self.calculate_gifts_cost()
        print(f"Remaining budget: {self.budget - gifts_total} PLN")
    
    def save_to_file(self, filename):
        data = {
            'celebrant': {'name': self.celebrant.name, 'age': self.celebrant.age},
            'date': self.date,
            'location': self.location,
            'budget': self.budget,
            'guests': [{'name': g.name, 'age': g.age} for g in self.guest_list],
            'tasks': [{
                'description': t.description,
                'deadline': t.deadline,
                'responsible_person': t.responsible_person.name,
                'status': t.status
            } for t in self.task_list]
        }
        
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"\nParty data saved to file {filename}")

def load_from_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        
        celebrant = Person(data['celebrant']['name'], data['celebrant']['age'])
        party = BirthdayParty(
            celebrant,
            data['date'],
            data['location'],
            data['budget']
        )
        
        # Adding guests
        for guest in data['guests']:
            party.add_guest(Person(guest['name'], guest['age']))
        
        # Adding tasks (simplified - assuming responsible persons are among guests)
        for task in data['tasks']:
            responsible = next((g for g in party.guest_list if g.name == task['responsible_person']), None)
            if responsible:
                t = Task(task['description'], task['deadline'], responsible)
                t.status = task['status']
                party.schedule_task(t)
        
        print(f"\nParty data loaded from file {filename}")
        return party
    
    except FileNotFoundError:
        print(f"File {filename} does not exist.")
        return None

def main():
    print("=== BIRTHDAY PARTY ORGANIZER ===")
    
    # Create celebrant
    print("\nEnter celebrant details:")
    name = input("Name: ")
    age = int(input("Age: "))
    celebrant = Person(name, age)
    
    # Create party
    date = input("Party date (e.g., 2023-12-31): ")
    location = input("Party location: ")
    budget = float(input("Party budget (PLN): "))
    party = BirthdayParty(celebrant, date, location, budget)
    
    while True:
        print("\n=== MAIN MENU ===")
        print("1. Manage guests")
        print("2. Manage gifts")
        print("3. Manage tasks")
        print("4. Party summary")
        print("5. Save data to file")
        print("6. Load data from file")
        print("7. Exit program")
        
        choice = input("Choose option (1-7): ")
        
        if choice == "1":
            while True:
                print("\n=== GUEST MANAGEMENT ===")
                print("1. Add guest")
                print("2. Remove guest")
                print("3. Show guest list")
                print("4. Return to main menu")
                
                guest_choice = input("Choose option (1-4): ")
                
                if guest_choice == "1":
                    name = input("Guest name: ")
                    age = int(input("Guest age: "))
                    party.add_guest(Person(name, age))
                
                elif guest_choice == "2":
                    party.show_guests()
                    if party.guest_list:
                        num = int(input("Enter guest number to remove: ")) - 1
                        if 0 <= num < len(party.guest_list):
                            party.remove_guest(party.guest_list[num])
                        else:
                            print("Invalid guest number")
                
                elif guest_choice == "3":
                    party.show_guests()
                
                elif guest_choice == "4":
                    break
                
                else:
                    print("Invalid choice")
        
        elif choice == "2":
            while True:
                print("\n=== GIFT MANAGEMENT ===")
                print("1. Add gift")
                print("2. Show celebrant's gifts")
                print("3. Show specific guest's gifts")
                print("4. Return to main menu")
                
                gift_choice = input("Choose option (1-4): ")
                
                if gift_choice == "1":
                    party.show_guests()
                    if not party.guest_list:
                        print("Add guests first")
                        continue
                    
                    giver_num = int(input("Enter gift giver's number: ")) - 1
                    if 0 <= giver_num < len(party.guest_list):
                        giver = party.guest_list[giver_num]
                        
                        print("\nGift recipient:")
                        print("1. Celebrant")
                        print("2. Another guest")
                        recipient_type = input("Choose option (1-2): ")
                        
                        if recipient_type == "1":
                            recipient = party.celebrant
                        elif recipient_type == "2":
                            party.show_guests()
                            recipient_num = int(input("Enter recipient's number: ")) - 1
                            if 0 <= recipient_num < len(party.guest_list):
                                recipient = party.guest_list[recipient_num]
                            else:
                                print("Invalid guest number")
                                continue
                        else:
                            print("Invalid choice")
                            continue
                        
                        name = input("Gift name: ")
                        price = float(input("Gift price (PLN): "))
                        
                        gift = Gift(name, price, giver, recipient)
                        recipient.add_gift(gift)
                        print(f"Added gift: {name}")
                    
                    else:
                        print("Invalid guest number")
                
                elif gift_choice == "2":
                    party.celebrant.show_gifts()
                
                elif gift_choice == "3":
                    party.show_guests()
                    if party.guest_list:
                        num = int(input("Enter guest number: ")) - 1
                        if 0 <= num < len(party.guest_list):
                            party.guest_list[num].show_gifts()
                        else:
                            print("Invalid guest number")
                
                elif gift_choice == "4":
                    break
                
                else:
                    print("Invalid choice")
        
        elif choice == "3":
            while True:
                print("\n=== TASK MANAGEMENT ===")
                print("1. Add task")
                print("2. Mark task as done")
                print("3. Show task list")
                print("4. Return to main menu")
                
                task_choice = input("Choose option (1-4): ")
                
                if task_choice == "1":
                    description = input("Task description: ")
                    deadline = input("Deadline (e.g., 2023-12-31): ")
                    
                    party.show_guests()
                    if not party.guest_list:
                        print("Add guests first")
                        continue
                    
                    num = int(input("Enter responsible person's number: ")) - 1
                    if 0 <= num < len(party.guest_list):
                        responsible = party.guest_list[num]
                        task = Task(description, deadline, responsible)
                        party.schedule_task(task)
                    else:
                        print("Invalid guest number")
                
                elif task_choice == "2":
                    party.show_tasks()
                    if party.task_list:
                        num = int(input("Enter task number to mark: ")) - 1
                        if 0 <= num < len(party.task_list):
                            party.task_list[num].mark_as_done()
                        else:
                            print("Invalid task number")
                
                elif task_choice == "3":
                    party.show_tasks()
                
                elif task_choice == "4":
                    break
                
                else:
                    print("Invalid choice")
        
        elif choice == "4":
            party.show_summary()
        
        elif choice == "5":
            filename = input("Enter filename to save (e.g., party.json): ")
            party.save_to_file(filename)
        
        elif choice == "6":
            filename = input("Enter filename to load (e.g., party.json): ")
            new_party = load_from_file(filename)
            if new_party:
                party = new_party
        
        elif choice == "7":
            print("Closing program...")
            break
        
        else:
            print("Invalid choice. Please choose option 1-7.")

if __name__ == "__main__":
    main()