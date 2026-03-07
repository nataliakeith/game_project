import mysql.connector
import random

connection = mysql.connector.connect(host="127.0.0.1",
            port=3306,
            database="flight_game",
            user="root",
            password='y""o32',
            autocommit=True)
cursor = connection.cursor(dictionary=True)

#this line is to fix bothv values in the tables that was error
cursor.execute("update false_ticket set flight_time=%s where ticket_id=50;", ("00:00",))
cursor.execute("update false_ticket set flight_date=%s where ticket_id=38;", ("2026-03-12",))
connection.commit()

#this is to generate airport names for tickets
cursor.execute("update regular_ticket set departure_airport=(select name from airport order by rand() limit 1), arrival_airport=(select name from airport order by rand() limit 1);")
cursor.execute("update false_ticket set departure_airport=(select name from airport order by rand() limit 1), arrival_airport=(select name from airport order by rand() limit 1);")
connection.commit()

# this for humans and aliens generating
cursor.execute("select * from passenger where true_species=1 order by rand() limit 14;")
humans = cursor.fetchall()
cursor.execute("select * from passenger where true_species=0 order by rand() limit 7;")
aliens = cursor.fetchall()
passengers = humans + aliens
random.shuffle(passengers)

#the dates and correspoding ids, this can't be change, otherwise will be broken if ppl get on huamns wrong dates
regular_ticket_dates = {"01": (1, 11), "03": (12, 23), "05": (24, 36), "06": (37, 50), "09": (51, 67), "12": (68, 86), "15": (87, 99)}
false_ticket_dates = {"01": (1, 14), "03": (15, 34), "05": (49, 63), "06": (64, 77), "09": (78, 88), "12": (89, 99), "15": (35, 48)}
days = ["01", "03", "05", "06", "09", "12", "15"]

#intro that player gets
def intro():
        print("==========================================================================================")
        print("Strange and disturbing events have been occurring all around the globe.")
        print("After months of investigation, Earth Defense Intelligence Bureau have discovered the truth:")
        print("aliens have infiltrated Earth, disguising themselves as humans.")
        print()
        print("You have been assigned to airport border control to investigate these suspected infiltrators.")
        print("Your mission is to identify the impostors before they enter the country.")
        print("Be careful. They look like us.")
        print("They behave like us.")
        print("But they are not one of us.")
        print("Stop them before it's too late — the fate of Earth depends on you.")
        print("==========================================================================================")

        input("Press Enter to start...")

#this part of the code i needed AI help, so i'm not fully familiar with this, since whatever i tried didnt work
import string
from datetime import date, timedelta

#fetch airport names from country
cursor.execute("select name from country;")
countries = [row["name"] for row in cursor.fetchall()]

#select passenger true species and passport
cursor.execute("select passport.passport_ID, passenger.true_species from passport join passenger on passport.passenger_ID = passenger.id;")

passports = cursor.fetchall()

for row in passports: #humans passport has k=2 so 2 uppercase letter and 6 digits, theya re joined into string, expiration
    #date pick random days between 1 year and 10 years, this can be change,
    if row["true_species"] == 1:
        passport_number = "".join(random.choices(string.ascii_uppercase, k=2)) + "".join(random.choices(string.digits, k=6))
        issuing_country = random.choice(countries)
        expiration_date = (date.today() + timedelta(days=random.randint(365, 3650))).isoformat()
    else:#aliens passport have up to 8 digits, 5 letter s+ 3 digits, the expiration rnage is much
        #compared to humasn, expiration date will give expired passports
        passport_number = random.choice([
            "AA000000",
            "".join(random.choices(string.digits, k=8)),
            "".join(random.choices(string.ascii_uppercase, k=5)) + "".join(random.choices(string.digits, k=3)),])
        issuing_country = random.choice(countries)
        expiration_date = (date.today() - timedelta(days=random.randint(100, 2000))).isoformat()

    cursor.execute(
        "update passport set passport_number=%s, issuing_country=%s, expiration_date=%s where passport_ID=%s;",
        (passport_number, issuing_country, expiration_date, row["passport_ID"])
    )

connection.commit()

def tutorial(): #this function is for game tutorial, it ried putting a text in the elif, but didnt work, function worked tho
    print("How to identify anomalies")
    print("1. Passport expiration date: Some passengers have expired passports or odd dates")
    print("2. Passport number format: Some passengers have odd format, with uncommon number of digits and letters")
    print("3. Age: Some passengers might have unmatching age to birth date")
    print("4.Boosts: Boosts are given by aliens with a good heart, they reveal surprise factor which give you further information on the passenger true species.")
    print("Be aware that alien presence affects airport sustainability and reputation, and if too many pass, you lose.")

#end of the part im confused about haha, but yea, this is to add values to the passport_number, issuing_country, expiraiton date

def generate_cards(cursor, passenger_id, ticket_table, ticket_id):

#function for game cards
    cursor.execute("select description, surprise_factor, age from passenger where id=%s;", (passenger_id,))
    character = cursor.fetchone()

    cursor.execute("select true_species from passenger where id=%s;", (passenger_id,))
    passenger_true_species = cursor.fetchone()["true_species"]

    print("----------------------------------------")
    print("PASSENGER APPROACHING...")
    print("Description:", character["description"])
    print("----------------------------------------")

#calls passport
    print('You: "Hello. Passport control. May I see your passport?"')

    cursor.execute(
        "select passenger.last_name, passenger.first_name, passenger.nationality, passenger.birth_date, passenger.sex, passenger.place_birth, passenger.age, passport.passport_number, passport.issuing_country, passport.expiration_date "
        "from passenger join passport on passport.passenger_ID=passenger.id where passenger.id=%s;",
        (passenger_id,)
    )
    passport = cursor.fetchone()

    print("PASSPORT")
    print("Surname:", passport["last_name"])
    print("Given names:", passport["first_name"])
    print("Nationality:", passport["nationality"])
    print("Date of birth:", passport["birth_date"])
    print("Sex:", passport["sex"])
    print("Place of birth:", passport["place_birth"])
    print("Passport Nº:", passport["passport_number"])
    print("Issuing Country:", passport["issuing_country"])
    print("Date of expiry:", passport["expiration_date"])

 #options to ask once you see passport
    while True:
        print("Options:")
        print("1) Ask for age")
        print("2) Ask for ticket")
        print("3) Use boost (check for surprise factor)") #we should add how aliens will give us boost, to use to see surprise factor, so this should be block if u dont have boost.
        print("4) Next passenger")
        print("5) APPROVE passenger")
        print("6) DENY passenger")
        print("7) Tutorial")

        choice = input("Choose 1-7: ")

        if choice == "1":
            print('You: "What is your age?"')
            print("Passenger says:", passport["age"])

        elif choice == "2":
            print('You: "Show me your ticket."')
            cursor.execute(f"select departure_airport, arrival_airport, flight_date, flight_time, seat from {ticket_table} where ticket_id=%s;",
                           (ticket_id,))
            ticket = cursor.fetchone()

            print("TICKET")
            print("Departure airport:", ticket["departure_airport"])
            print("Arrival airport:", ticket["arrival_airport"])
            print("Flight date:", ticket["flight_date"])
            print("Flight time:", ticket["flight_time"])
            print("Seat:", ticket["seat"])

        elif choice == "3":
            print("BOOST RESULT")
            print("Surprise factor:", character["surprise_factor"])

        elif choice == "4":
            return ("none", passenger_true_species)

        elif choice == "5":
            return ("approve", passenger_true_species)

        elif choice == "6":
            return ("deny", passenger_true_species)

        elif choice == "7":
            tutorial()
            continue
        else:
            print("Invalid. Type 1-7.")

def day_summary(day, approved_humans, denied_humans, approved_aliens, denied_aliens):
    print("======================")
    print("DAY SUMMARY:", day, "DECEMBER")
    print("======================")
    print("Humans approved:", approved_humans)
    print("Humans denied:", denied_humans)
    print("ALIENS PASSED(DANGER ALERT):", approved_aliens)
    print("Aliens denied:", denied_aliens)
    print("======================")

intro() #dont remove this, im caling function now, so player sees the tiny story itnroduction
#loop for generating days and 3 case sper day
passenger_index = 0

for day in days:
    print("======================")
    print("DAY:", day, "DECEMBER")
    print("======================")

    approved_humans = 0
    denied_humans = 0
    approved_aliens = 0
    denied_aliens = 0

    passengers_of_day = passengers[passenger_index:passenger_index + 3]
    passenger_index += 3

    for passenger in passengers_of_day:
        if passenger["true_species"] == 1:
            ticket_range = regular_ticket_dates[day]
            ticket_table = "regular_ticket"
        else:
            ticket_range = false_ticket_dates[day]
            ticket_table = "false_ticket"

        ticket_id = random.randint(ticket_range[0], ticket_range[1])
        decision, true_species = generate_cards(cursor, passenger["id"], ticket_table, ticket_id)

        if decision == "approve":
            if true_species == 1:
                approved_humans += 1
            else:
                approved_aliens += 1

        elif decision == "deny":
            if true_species == 1:
                denied_humans += 1
            else:
                denied_aliens += 1

    day_summary(day, approved_humans, denied_humans, approved_aliens, denied_aliens)

cursor.close()
connection.close()



