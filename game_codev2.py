import mysql.connector
import random
from dotenv import load_dotenv
import os

load_dotenv()

connection = mysql.connector.connect(host="127.0.0.1",
            port=3306,
            database="flight_game",
            user="root",
            password= os.getenv("DB_PASSWORD"),
            autocommit=True)
cursor = connection.cursor(dictionary=True)

from systems.energy import update_energy
from systems.budget import update_budget
from systems.reputation import update_reputation, reputation_emoji
from systems.sustainability import update_sustainability
from systems.backstabber import check_backstabber, backstab
from session import count_aliens

cursor = connection.cursor(dictionary=True)

#this line is to fix both values in the tables that was NULL
cursor.execute("update false_ticket set flight_time=%s where ticket_id=50;", ("00:00",))
cursor.execute("update false_ticket set flight_date=%s where ticket_id=38;", ("2026-03-12",))
connection.commit()

#this is to generate airport names for tickets table, departure and arrival airports rows
cursor.execute("update regular_ticket set departure_airport=(select name from airport order by rand() limit 1), arrival_airport=(select name from airport order by rand() limit 1);")
cursor.execute("update false_ticket set departure_airport=(select name from airport order by rand() limit 1), arrival_airport=(select name from airport order by rand() limit 1);")
connection.commit()

#this part is for generating humans and aliens
cursor.execute("select * from passenger where true_species=1 order by rand() limit 14;")
humans = cursor.fetchall()
cursor.execute("select * from passenger where true_species=0 order by rand() limit 7;")
aliens = cursor.fetchall()
passengers = humans + aliens
random.shuffle(passengers)

#the dates and corresponding ids, so game runs with correct dates on the tables
regular_ticket_dates = {"01": (1, 11), "03": (12, 23), "05": (24, 36), "06": (37, 50), "09": (51, 67), "12": (68, 86), "15": (87, 99)}
false_ticket_dates = {"01": (1, 14), "03": (15, 34), "05": (49, 63), "06": (64, 77), "09": (78, 88), "12": (89, 99), "15": (35, 48)}
days = ["01", "03", "05", "06", "09", "12", "15"]

#intro that player gets
def intro():
        return {
        "lore" : ["Strange and disturbing events have been occurring all around the globe.",
        "After months of investigation, Earth Defense Intelligence Bureau have discovered the truth:",
        "aliens have infiltrated Earth, disguising themselves as humans.",
        "You have been assigned to airport border control to investigate these suspected infiltrators.",
        "Your mission is to identify the impostors before they enter the country.",
        "Be careful. They look like us.",
        "They behave like us.",
        "But they are not one of us.",
        "Stop them before it's too late — the fate of Earth depends on you.",
        ] }

        #("Press Enter to start...")

#this part I had to import for filling passport table information, passport number, issuing country and expiration date

import string
from datetime import date, timedelta

#fetch airport names from country
cursor.execute("select name from country;")
countries = [row["name"] for row in cursor.fetchall()]

#select passenger true species and passport
cursor.execute("select passport.passport_ID, passenger.true_species from passport join passenger on passport.passenger_ID = passenger.id;")

passports = cursor.fetchall()

for row in passports: #humans passport has k=2 so 2 uppercase letter and 6 digits, they're joined into string,
    # expiration date pick random days between 1 year and 10 years.
    if row["true_species"] == 1:
        passport_number = "".join(random.choices(string.ascii_uppercase, k=2)) + "".join(random.choices(string.digits, k=6))
        issuing_country = random.choice(countries)
        expiration_date = (date.today() + timedelta(days=random.randint(365, 3650))).isoformat()
    else:#aliens passport might have up to 8 digits, 5 uppercase letters, 3 digits, the expiration range is much lower
        #compared to humans, expiration date will give expired passports for aliens.
        passport_number = random.choice([
            "AA000000", "ZZ055689",
            "".join(random.choices(string.digits, k=8)),
            "".join(random.choices(string.ascii_uppercase, k=5)) + "".join(random.choices(string.digits, k=3)),])
        issuing_country = random.choice(countries)
        expiration_date = (date.today() - timedelta(days=random.randint(100, 2000))).isoformat()

    cursor.execute(
        "update passport set passport_number=%s, issuing_country=%s, expiration_date=%s where passport_ID=%s;",
        (passport_number, issuing_country, expiration_date, row["passport_ID"])
    )

connection.commit()

def tutorial(): #this function is for game tutorial.
    return {
    "tutorial": ["=====How to identify anomalies=====",
    "**Every alien will have one or more odd information that gives you clues about their true species**",
    "1. Passport expiration date: Humans always have expiration date between 1 and 10 years.",
    "2. Passport number format: Humans passports have 2 uppercase letters and 6 digits.",
    "3. Age: Some passengers might have unmatching age to birth date, that indicates a anomaly.",
    "4. Boosts: Boosts are given by aliens with a good heart, they reveal surprise factor which give you further information on the passenger true species.",
    "*Some of these creatures might fool you, choose wisely.",
    "5. False documents: Check for any uncommon typing in the documents the passenger presents to you, whether is ticket or passport.",
    "6. Description: Reading the description of the passenger might give you clues about who they are.",
    "**Be aware that aliens presence and events affects airport sustainability, energy, reputation and budget, if too many aliens pass, you lose**",
    ]}
#function to set maximum and minimum values to status
def max_state(state):
    if state["energy"] > 100:
        state["energy"] = 100
    if state["energy"] < 0:
        state["energy"] = 0

    if state["reputation"] > 100:
        state["reputation"] = 100
    if state["reputation"] < 0:
        state["reputation"] = 0

    if state["sustainability"] > 100:
        state["sustainability"] = 100
    if state["sustainability"] < 0:
        state["sustainability"] = 0

    if state["budget"] < 0:
        state["budget"] = 0

    return state
#function for game cards
def generate_cards(cursor, passenger_id, ticket_table, ticket_id, state):

    cursor.execute("select description, surprise_factor, age from passenger where id=%s;", (passenger_id,))
    character = cursor.fetchone()

    cursor.execute("select true_species from passenger where id=%s;", (passenger_id,))
    passenger_true_species = cursor.fetchone()["true_species"]

    description_data = {
        "header": "PASSENGER APPROACHING...",
        "description:": character["description"]
    }


    print("----------------------------------------")
    print("PASSENGER APPROACHING...")
    print("Description:", character["description"])
    print("----------------------------------------")

#calls passport

    print("========================================================")
    print('You: "Hello. Passport control. May I see your passport?"')
    print("========================================================")


    cursor.execute(
        "select passenger.last_name, passenger.first_name, passenger.nationality, passenger.birth_date, passenger.sex, passenger.place_birth, passenger.age, passport.passport_number, passport.issuing_country, passport.expiration_date "
        "from passenger join passport on passport.passenger_ID=passenger.id where passenger.id=%s;",
        (passenger_id,)
    )
    passport = cursor.fetchone()


    passport_data = {
    "surname": passport["last_name"],
    "given_names": passport["first_name"],
    "nationality": passport["nationality"],
    "date_of_birth": passport["birth_date"],
    "sex": passport["sex"],
    "place_of_birth": passport["place_birth"],
    "passport_number": passport["passport_number"],
    "issuing_country": passport["issuing_country"],
    "date_of_expiry": passport["expiration_date"]
    }


#Interactions available after seeing passport information
    while True:
        print()
        print("==========================")
        print("Options:")
        print("1) Ask for age")
        print("2) Ask for ticket")
        print("3) Use boost (check for surprise factor)")
        print("4) Next passenger")
        print("5) APPROVE passenger")
        print("6) DENY passenger")
        print("7) Tutorial")
        print("8) Check your status ")
        print("==========================")


        choice = input("Choose 1-8: ")
        print()

        if choice == "1":
            age_data = {
                "type": "age",
                "question": 'You: "What is your age?"',
                "answer": passport["age"]
            }
            print(age_data["question"])
            print("Passenger says:", age_data["answer"])


        elif choice == "2":

            if state["inspection_blocked"]:
                print("The inspection system is offline today")
            else:
                print('You: "Show me your ticket."')
                cursor.execute(f"select departure_airport, arrival_airport, flight_date, flight_time, seat from {ticket_table} where ticket_id=%s;",
                           (ticket_id,))
                ticket = cursor.fetchone()
                print("====TICKET====")
                print("Departure airport:", ticket["departure_airport"])
                print("Arrival airport:", ticket["arrival_airport"])
                print("Flight date:", ticket["flight_date"])
                print("Flight time:", ticket["flight_time"])
                print("Seat:", ticket["seat"])

                ticket_data = {
                    "departure_airport":  ticket["departure_airport"],
                    "arrival_airport": ticket["arrival_airport"],
                    "flight_date": ticket["flight_date"],
                    "flight_time": ticket["flight_time"],
                    "seat": ticket["seat"]
                }

            

        elif choice == "3":

            if state["surprise_boost_days"] > 0:
                print("***BOOST RESULT***")
                print("Surprise factor:", character["surprise_factor"])

            else:
                print("You have no boosts.")

            boost = {
                "boost": character["surprise_factor"]
            }

        elif choice == "4":
            return ("none", passenger_true_species)

        elif choice == "5":
            return ("approve", passenger_true_species)

        elif choice == "6":
            return ("deny", passenger_true_species)

        elif choice == "7":
            tutorial()
            continue

        elif choice == "8":
            print("Energy:", state["energy"])
            print("Budget:", state["budget"])
            print("Reputation:", state["reputation"], reputation_emoji(state["reputation"]))
            print("Sustainability:", state["sustainability"])
            print()

            status = {
                "energy": state["energy"],
                "budget": state["budget"],
                "reputation": state["reputation"],
                "reputation_emoji": reputation_emoji(state["reputation"]),
                "sustainability": state["sustainability"]
            }
        else:
            print("Invalid. Type 1-8.")


def day_summary(day, approved_humans, denied_humans, approved_aliens, denied_aliens):
    print()
    print("===============================")
    print("===============================")
    print("DAY SUMMARY:", day, "DECEMBER")
    print("===============================")
    print("Humans approved:", approved_humans)
    print("Humans denied:", denied_humans)
    print("ALIENS PASSED(DANGER ALERT):", approved_aliens)
    print("Aliens denied:", denied_aliens)
    print("===============================")
    print("===============================")
    print()
    day_sum = {
        "day_summary": day,
        "humans_approved": approved_humans,
        "humans_denied": denied_humans,
        "aliens_passed": approved_aliens,
        "aliens_denied": denied_aliens,


    }


#intro() #calling intro

state = {
    "energy": 100,
    "budget": 10000,                                                            #I added this so the game stores our stasts in a dictonary
    "reputation": 100,
    "sustainability": 100,
    "surprise_boost_days": 0,                                                    #TO COUNT DAYS OF BOOST LEFT!
    "inspection_blocked":False                                                   #FOR POTENTIAL TO BLOCK INSPECTION
}

passenger_index = 0

def day_intro(day, state):
        return {
            "day": f"{day} DECEMBER",
            "energy": state["energy"],
            "budget": state["budget"],
            "reputation": state["reputation"],
            "reputation_emoji": reputation_emoji(state["reputation"]),
            "sustainability": state["sustainability"]
        }

    # state["inspection_blocked"] = False                              #IF WE GET THE BLOCK INSPECTION EVENT.RESETS BLOCKED INSPECTION JUST IN CASE

    # from systems.events import daily_event                           #PER DAY WE GET A DAILY EVENT

    # state = daily_event(state)                                           
 #generating 3 passengers per day, out of the 21 previously generated passengers.
if __name__ == '__main__':
    intro()
    passenger_index = 0
    for day in days:
        print()
        print("======================")
        print("======================")
        print("DAY:", day, "DECEMBER")
        print("======================")
        print("======================")
        print()
        print("Energy:", state["energy"])
        print("Budget:", state["budget"])
        print("Reputation:", state["reputation"], reputation_emoji(state["reputation"]))
        print("Sustainability:", state["sustainability"])
        print()

        day_intro_data = day_intro(day, state)

        approved_humans = 0
        denied_humans = 0
        approved_aliens = 0
        denied_aliens = 0

        passengers_of_day = passengers[passenger_index:passenger_index + 3]
        passenger_index += 3

        for passenger in passengers_of_day:

            if passenger["true_species"] == 0 and check_backstabber():
                state, day_knocked_out = backstab(state)

                if day_knocked_out:
                    break

            if passenger["true_species"] == 1:
                ticket_range = regular_ticket_dates[day]
                ticket_table = "regular_ticket"
            else:
                ticket_range = false_ticket_dates[day]
                ticket_table = "false_ticket"

            ticket_id = random.randint(ticket_range[0], ticket_range[1])
            decision, true_species = generate_cards(cursor, passenger["id"], ticket_table, ticket_id, state)

            if decision == "approve":
                cursor.execute(
                    "UPDATE session SET allowed_in = 1 WHERE passenger_id = %s",
                    (passenger["id"],)
                )

            elif decision == "deny":
                cursor.execute(
                    "UPDATE session SET allowed_in = 0 WHERE passenger_id = %s",
                    (passenger["id"],)
                )

            connection.commit()

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

        state["inspection_blocked"] = False

        from systems.events import daily_event

        state = daily_event(state)

        state = max_state(state)

        alien_count = count_aliens(connection)

        state["energy"] = update_energy(state["energy"], alien_count)
        state["sustainability"] = update_sustainability(state["sustainability"], alien_count)
        state["reputation"] = update_reputation(state["reputation"], alien_count, state["sustainability"])
        state["budget"] = update_budget(state["budget"], state["reputation"], state["sustainability"])

        state = max_state(state)

        if state["energy"] <= 0:
            print("Out of energy.The airport shut down and the aliens took over.")
            print("GAME OVER")
            break

        if state["reputation"] <= 0:
            print("People don't trust the airport anymore.The government has cut funding and the airport shut down.")
            print("GAME OVER")
            break

        if state["sustainability"] < 30 and state["budget"] <= 0:
            print("Airport sustainability has dropped below acceptable levels.The government has abandoned the airport.")
            print("GAME OVER")
            break

        if state["surprise_boost_days"] > 0:
            state["surprise_boost_days"] -= 1



    cursor.close()
    connection.close()



