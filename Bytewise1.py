print("People i know")

friends="Muneeb,Faiz,Jahanzaib"
print(friends)

number = 30
new_num = number + 11
print(new_num)

author = "Kafka"
author2 = " Dostoevsky"

Both = author + author2
print(Both)
print(author + author2)
print("Hello, World ! " + author +" is my favourite author")

number_of_husbands = 2

if number_of_husbands == 1:
    print("So far so good.")
    print("Congratulations.")
print("All done")

print("LOTTERY TICKET")

your_ticket_number = 134556

if your_ticket_number != 487208:
    print("Better luck next time.")

species = "cat"
color = "black"

if species == "cat" and color == "white":
    print("Yep, we'll keep it.")
elif species == "dog" and color == "black":
    print("It's a black dog so i want it")    
else:
    print("Nope, dont want it.")

 # This is a comment.
 # Comments don't show in the output.    

'''
Print("rayyan")
abdullah

'''

cities = ["Atlanta", "Baltimore", "Chicago","Dallas","Texas"]
print("Printing all the cities: ")

cities.append("New York")

smaller_list_of_cities = cities[2:]


city_to_check = input("Enter the name of a city: ")
city_found = False

for city in cities:
    if city_to_check == city:
        city_found = True
        break

if city_found:
    print("It's among the list")
else:
    print("Invalid Answer")



# Print each element in the list
# print(" Printing each element: ")
# for city in cities:
#     print(city)


monthly_income = input(" Enter your monthly income: ")
monthly_income_as_an_integer = int(monthly_income)
yearly_income = monthly_income_as_an_integer * 12
print(yearly_income)


customer_29876 = {"first name": "David", "lastname": "Elliott", "address": "4803 Wellesley St."}
#first name is a key and david is a value
address_of_customer = customer_29876["address"]
print("Address of the customer is : " + address_of_customer)


for each_value in customer_29876.values():
    print(each_value)

    

# list of dictionaries
customer_29876 = {
 "first name": "David",
 "last name": "Elliott",
 "address": "4803 Wellesley St.",
 }


customers = [
    {
        "customer id": 0,
        "first name":"John",
        "last name": "Ogden",
        "address": "301 Arbor Rd.",
    },
    {
        "customer id": 1,
        "first name":"Ann",
        "last name": "Sattermyer",
        "address": "PO Box 1145",
    },
    {
        "customer id": 2,
        "first name":"Jill",
        "last name": "Somers",
        "address": "3 Main St.",
    }
 ]


dictionary_to_look_in = customers[1]
customer_address = dictionary_to_look_in["address"]

# To learn how many dictionaries are in the list, we measure the list's length.

new_customer_id = len(customers)


# creating a list within a dictionary
customer_29876 = {
 "first name": "David",
 "last name": "Elliott",
 "address": "4803 Wellesley St.",
 "discounts": ["standard", "volume", "loyalty"],
 }


# using the list within the dictionary
 
if "brother-in-law" in customer_29876["discounts"]:
 discount_amount = .30
elif "loyalty" in customer_29876["discounts"]:
 discount_amount = .15
elif "volume" in customer_29876["discounts"]:
 discount_amount = .10
elif "standard" in customer_29876["discounts"]:
 discount_amount = .05

 # each dictionary has a key value and here 0 1 and 2 are the key values 
 # dictionary within a dictionary

 customers = {
     0: {
            "first name":"John",
            "last name": "Ogden",
            "address": "301 Arbor Rd.",
        },
     1: {
            "first name":"Ann",
            "last name": "Sattermyer",
            "address": "PO Box 1145",
        },
     2: {
            "first name":"Jill",
            "last name": "Somers",
            "address": "3 Main St.",
        },
 }

# this prints everything in the dictionary
 print(customers[2])
 # this prints just the address within the dictionary
 print(customers[2]["address"])

 # Functions
 def add_numbers():
  first_number = 2
  second_number = 3
  total = first_number + second_number
  print(total)


