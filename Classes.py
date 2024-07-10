# say_if_minor as a standalone function

class Patient():
    def __init__(self, last_name, first_name, age):
        self.last_name = last_name
        self.first_name = first_name
        self.age = age

pid4343 = Patient("Taleb", "Zayn", 20)
pid4344 = Patient("Anand", "Mia", 32)
pid4345 = Patient("Oppenheimer", "Robert", 44)

def say_if_minor(patient_first_name,patient_last_name, patient_age):
    if patient_age < 21:
        print(patient_first_name + " " +patient_last_name + " is a minor")


print(pid4343.age)
say_if_minor(pid4343.first_name,pid4343.last_name,pid4343.age)



# say_if_minor to a method of the Patient class

class Patient():
    def __init__(self, last_name, first_name, age):
        self.last_name = last_name
        self.first_name = first_name
        self.age = age

    def say_if_minor(self):
        if self.age < 21:
            print(self.first_name + " " + self.last_name + " is a minor")

pid4343 = Patient("Taleb", "Zayn", 20)
pid4344 = Patient("Anand", "Mia", 32)
pid4345 = Patient("Oppenheimer", "Robert", 44)

print(pid4343.age)
pid4343.say_if_minor()

with open("whatever.txt", "w") as f:
    f.write("This is a line of text.\n")
    f.write("This is another line of text.\n")

with open("whatever.txt", "r") as f:
    contents = f.read()
    print(contents)
