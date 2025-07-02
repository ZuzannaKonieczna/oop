import json

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.gifts = []

    def add_gift(self, gift):
        self.gifts.append(gift)

    def show_gifts(self):
        print(f"\nGifts received by {self.name}:")
        if not self.gifts:
            print("No gifts.")
            return
        for i, gift in enumerate(self.gifts, 1):
            print(f"{i}. {gift.name} (from {gift.giver.name}) - {gift.price} PLN")

    def __str__(self):
        return f"{self.name} ({self.age} years old)"

class Gift:
    def __init__(self, name, price, giver, recipient):
        self.name = name
        self.price = price
        self.giver = giver
        self.recipient = recipient

class Task:
    def __init__(self, description, deadline, responsible_person):
        self.description = description
        self.deadline = deadline
        self.responsible_person = responsible_person
        self.status = "Not done"

    def mark_done(self):
        self.status = "Done"
        print(f"Task '{self.description}' marked as done.")

    def __str__(self):
        return f"{self.description} (Deadline: {self.deadline}, Responsible: {self.responsible_person.name}, Status: {self.status})"

class BirthdayParty:
    def __init__(self, celebrant, date, location, budget):
        self.celebrant = celebrant
        self.date = date
        self.location = location
        self.budget = budget
        self.guests = []
        self.tasks = []

    def add_guest(self, guest):
        if guest not in self.guests:
            self.guests.append(guest)
            print(f"Guest '{guest.name}' added.")
        else:
            print(f"{guest.name} is already on the guest list.")

    def remove_guest(self, guest):
        if guest in self.guests:
            self.guests.remove(guest)
            print(f"Guest '{guest.name}' removed.")
        else:
            print(f"{guest.name} is not on the guest list.")

    def add_task(self, task):
        self.tasks.append(task)
        print(f"Task '{task.description}' added.")

    def show_tasks(self):
        print("\nTask List:")
        if not self.tasks:
            print("No tasks added.")
            return
        for i, task in enumerate(self.tasks, 1):
            print(f"{i}. {task}")

    def show_guests(self):
        print("\nGuest List:")
        if not self.guests:
            print("No guests added.")
            return
        for i, guest in enumerate(self.guests, 1):
            print(f"{i}. {guest}")

    def total_gift_cost(self):
        total = sum(gift.price for person in [self.celebrant] + self.guests for gift in person.gifts)
        print(f"\nTotal value of all gifts: {total} PLN")
        return total

    def show_summary(self):
        print("\n=== PARTY SUMMARY ===")
        print(f"Celebrant: {self.celebrant}")
        print(f"Date: {self.date}")
        print(f"Location: {self.location}")
        print(f"Budget: {self.budget} PLN")
        self.show_guests()
        self.show_tasks()
        total = self.total_gift_cost()
        print(f"Remaining budget: {self.budget - total} PLN")

    def save_to_file(self, filename):
        data = {
            'celebrant': {'name': self.celebrant.name, 'age': self.celebrant.age},
            'date': self.date,
            'location': self.location,
            'budget': self.budget,
            'guests': [{'name': g.name, 'age': g.age} for g in self.guests],
            'tasks': [{
                'description': t.description,
                'deadline': t.deadline,
                'responsible_person': t.responsible_person.name,
                'status': t.status
            } for t in self.tasks]
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"\nData saved to '{filename}'.")

def load_party(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)

        celebrant = Person(data['celebrant']['name'], data['celebrant']['age'])
        party = BirthdayParty(celebrant, data['date'], data['location'], data['budget'])

        for g in data['guests']:
            party.add_guest(Person(g['name'], g['age']))

        for t in data['tasks']:
            responsible = next((g for g in party.guests if g.name == t['responsible_person']), None)
            if responsible:
                task = Task(t['description'], t['deadline'], responsible)
                task.status = t['status']
                party.add_task(task)

        print(f"\nData loaded from '{filename}'.")
        return party
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None

def choose_person(people):
    for i, p in enumerate(people, 1):
        print(f"{i}. {p}")
    idx = int(input("Enter number: ")) - 1
    return people[idx] if 0 <= idx < len(people) else None

def main():
    print("=== BIRTHDAY PARTY ORGANIZER ===")
    print("1. Load party from file")
    print("2. Create new party")
    option = input("Choose 1 or 2: ")

    if option == "1":
        file = input("Filename: ")
        party = load_party(file)
        if not party:
            return
    elif option == "2":
        name = input("Celebrant's name: ")
        age = int(input("Celebrant's age: "))
        celebrant = Person(name, age)
        date = input("Party date (YYYY-MM-DD): ")
        location = input("Location: ")
        budget = float(input("Budget for gifts (PLN): "))
        party = BirthdayParty(celebrant, date, location, budget)
    else:
        print("Invalid option.")
        return

    while True:
        print("\n=== MAIN MENU ===")
        print("1. Manage guests")
        print("2. Manage gifts")
        print("3. Manage tasks")
        print("4. Show summary")
        print("5. Save to file")
        print("6. Exit")
        choice = input("Choose option: ")

        if choice == "1":
            while True:
                print("\n-- Guest Menu --")
                print("1. Add guest")
                print("2. Remove guest")
                print("3. Show guests")
                print("4. Back")
                g = input("Option: ")
                if g == "1":
                    name = input("Guest name: ")
                    age = int(input("Guest age: "))
                    party.add_guest(Person(name, age))
                elif g == "2":
                    guest = choose_person(party.guests)
                    if guest:
                        party.remove_guest(guest)
                elif g == "3":
                    party.show_guests()
                elif g == "4":
                    break
                else:
                    print("Invalid option.")

        elif choice == "2":
            while True:
                print("\n-- Gift Menu --")
                print("1. Add gift")
                print("2. Show celebrant's gifts")
                print("3. Show guest's gifts")
                print("4. Back")
                g = input("Option: ")
                if g == "1":
                    if not party.guests:
                        print("No guests available.")
                        continue
                    print("Select gift giver:")
                    giver = choose_person(party.guests)
                    if not giver:
                        continue
                    print("Gift recipient:")
                    print("1. Celebrant")
                    print("2. Guest")
                    r = input("Choose 1 or 2: ")
                    recipient = party.celebrant if r == "1" else choose_person(party.guests)
                    if not recipient:
                        continue
                    name = input("Gift name: ")
                    price = float(input("Gift price (PLN): "))
                    gift = Gift(name, price, giver, recipient)
                    recipient.add_gift(gift)
                    print("Gift added.")
                elif g == "2":
                    party.celebrant.show_gifts()
                elif g == "3":
                    print("Choose wich guest presents you wanna see: ")
                    guest = choose_person(party.guests)
                    if guest:
                        guest.show_gifts()
                elif g == "4":
                    break
                else:
                    print("Invalid option.")

        elif choice == "3":
            while True:
                print("\n-- Task Menu --")
                print("1. Add task")
                print("2. Mark task as done")
                print("3. Show tasks")
                print("4. Back")
                t = input("Option: ")
                if t == "1":
                    desc = input("Task description: ")
                    deadline = input("Deadline (YYYY-MM-DD): ")
                    print("Assign to:")
                    responsible = choose_person(party.guests)
                    if responsible:
                        party.add_task(Task(desc, deadline, responsible))
                elif t == "2":
                    party.show_tasks()
                    idx = int(input("Task number: ")) - 1
                    if 0 <= idx < len(party.tasks):
                        party.tasks[idx].mark_done()
                elif t == "3":
                    party.show_tasks()
                elif t == "4":
                    break
                else:
                    print("Invalid option.")

        elif choice == "4":
            party.show_summary()

        elif choice == "5":
            filename = input("Filename to save (e.g., party.json): ")
            party.save_to_file(filename)

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
