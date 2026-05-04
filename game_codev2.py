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
from systems.backstabber import check_backstabber

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
import string
from datetime import date, timedelta


#fetch airport names from country
cursor.execute("select name from country;")
countries = [row["name"] for row in cursor.fetchall()]

#select passenger true species and passport
cursor.execute("select passport.passport_ID, passenger.true_species from passport join passenger on passport.passenger_ID = passenger.id;")

passports = cursor.fetchall()

for row in passports: #humans passport has k=2 so 2 uppercase letter and 6 digits, they're joined into string,
    # expiration date pick random days between 1 and 10 years.
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

#the dates and corresponding ids, so game runs with correct dates on the tables
regular_ticket_dates = {"01": (1, 11), "03": (12, 23), "05": (24, 36), "06": (37, 50), "09": (51, 67), "12": (68, 86), "15": (87, 99)}
false_ticket_dates = {"01": (1, 14), "03": (15, 34), "05": (49, 63), "06": (64, 77), "09": (78, 88), "12": (89, 99), "15": (35, 48)}
days = ["01", "03", "05", "06", "09", "12", "15"]

state = {
    "energy": 100,
    "budget": 10000,                                                            #Game stores our stats in a dictonary
    "reputation": 100,
    "sustainability": 100,
    "surprise_boost_days": 0,                                                    #TO COUNT DAYS OF BOOST LEFT!
    "inspection_blocked":False                                                   #FOR POTENTIAL TO BLOCK INSPECTION
}

passenger_index = 0
total_approved_aliens = 0
current_backstabber = {}
current_game_data = {}
current_daily_event = {}

current_day_index = 0
passengers_checked_today = 0

approved_humans = 0
denied_humans = 0
approved_aliens = 0
denied_aliens = 0

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

def get_current_status():
    return {
        "energy": state["energy"],
        "budget": state["budget"],
        "reputation": state["reputation"],
        "reputation_emoji": reputation_emoji(state["reputation"]),
        "sustainability": state["sustainability"]
    }

def get_current_ticket_data():
    return current_game_data

def get_boost_status():
    return {
        "boost_days": state["surprise_boost_days"]
    }

def get_current_passenger_passport():
    passenger = passengers[passenger_index]

    cursor.execute(
        "SELECT passenger.last_name, passenger.first_name, passenger.nationality, passenger.birth_date, passenger.sex, passenger.place_birth, passport.passport_number, passport.issuing_country, passport.expiration_date "
        "FROM passenger JOIN passport ON passport.passenger_ID = passenger.id WHERE passenger.id=%s;",
        (passenger["id"],)
    )

    passport = cursor.fetchone()

    return {
        "surname": passport["last_name"],
        "given_names": passport["first_name"],
        "nationality": passport["nationality"],
        "birth_date": str(passport["birth_date"]),
        "sex": passport["sex"],
        "place_of_birth": passport["place_birth"],
        "passport_number": passport["passport_number"],
        "issuing_country": passport["issuing_country"],
        "expiration_date": str(passport["expiration_date"])
    }


def get_current_passenger_data():
    global current_game_data

    passenger = passengers[passenger_index]
    day = days[current_day_index]

    if current_game_data == {}:
        if passenger["true_species"] == 1:
            ticket_range = regular_ticket_dates[day]
            ticket_table = "regular_ticket"
        else:
            ticket_range = false_ticket_dates[day]
            ticket_table = "false_ticket"

        ticket_id = random.randint(ticket_range[0], ticket_range[1])

        cursor.execute(
            f"select departure_airport, arrival_airport, flight_date, flight_time, seat from {ticket_table} where ticket_id=%s;",
            (ticket_id,)
        )
        ticket = cursor.fetchone()

        current_game_data = {
            "departure_airport": ticket["departure_airport"],
            "arrival_airport": ticket["arrival_airport"],
            "flight_date": str(ticket["flight_date"]),
            "flight_time": str(ticket["flight_time"]),
            "seat": ticket["seat"]
        }

    cursor.execute(
        "select description, surprise_factor, age from passenger where id=%s;",
        (passenger["id"],)
    )
    character = cursor.fetchone()

    return {
        "header": "PASSENGER APPROACHING...",
        "description": character["description"]
    }


def get_current_passenger_age():
    passenger = passengers[passenger_index]

    cursor.execute(
        "select age from passenger where id=%s;",
        (passenger["id"],)

    )
    result = cursor.fetchone()

    return {
        "question": 'You: "What is your age?"',
        "answer": result["age"]
    }


def get_current_passenger_full_data():
    global current_backstabber

    if current_day_index >= len(days) or passenger_index >= len(passengers):
        return {
            "game_finished": True,
            "status": get_current_status(),
            "ending": get_ending()
        }
    passenger = passengers[passenger_index]

    if passenger["true_species"] == 0 and check_backstabber():
        current_backstabber = create_backstabber_event()
        return {
            "is_backstabber": True,
            "backstabber": current_backstabber,
            "status": get_current_status(),
            "day": days[current_day_index]
        }
    return {
        "is_backstabber": False,
        "description": get_current_passenger_data(),
        "passport": get_current_passenger_passport(),
        "status": get_current_status(),
        "ticket": get_current_ticket_data(),
        "day": days[current_day_index]
    }


def handle_decision(decision):
    global approved_humans, denied_humans, approved_aliens, denied_aliens, total_approved_aliens
    global passenger_index, passengers_checked_today, current_game_data, current_day_index, state

    passenger = passengers[passenger_index]
    true_species = passenger["true_species"]

    if decision == "approve":
        cursor.execute(
            "UPDATE session SET allowed_in = 1 WHERE passenger_id = %s",
            (passenger["id"],)
        )

        if true_species == 1:
            approved_humans += 1
        else:
            approved_aliens += 1
            total_approved_aliens += 1

    elif decision == "deny":
        cursor.execute(
            "UPDATE session SET allowed_in = 0 WHERE passenger_id = %s",
            (passenger["id"],)
        )

        if true_species == 1:
            denied_humans += 1
        else:
            denied_aliens += 1


    connection.commit()

    passenger_index += 1
    passengers_checked_today += 1
    current_game_data = {}

    return continue_after_passenger()


def continue_after_passenger():
    global current_daily_event, state
    global current_day_index, passengers_checked_today
    global approved_humans, denied_humans, approved_aliens, denied_aliens

    if passengers_checked_today == 3:
        human_count = approved_humans
        alien_count = approved_aliens
        wrong_denials = denied_humans

        state["energy"] = update_energy(state["energy"], alien_count)
        state["sustainability"] = update_sustainability(state["sustainability"], alien_count)
        state["reputation"] = update_reputation(
            state["reputation"],
            alien_count,
            state["sustainability"]
        )
        state["budget"] = update_budget(
            state["budget"],
            state["reputation"],
            state["sustainability"]
        )

        # decision effects
        state["reputation"] += human_count * 2
        state["reputation"] -= wrong_denials * 10
        state["budget"] += human_count * 200
        state["reputation"] += denied_aliens * 3

        state = max_state(state)

        summary_approved_humans = approved_humans
        summary_denied_humans = denied_humans
        summary_approved_aliens = approved_aliens
        summary_denied_aliens = denied_aliens

        # daily event after day 3 and day 6 only
        if (current_day_index + 1) % 3 == 0 and current_day_index != len(days) - 1:
            current_daily_event = create_daily_event()

            return {
                "day_finished": True,
                "show_event": True,
                "event": current_daily_event,
                "approved_humans": summary_approved_humans,
                "denied_humans": summary_denied_humans,
                "approved_aliens": summary_approved_aliens,
                "denied_aliens": summary_denied_aliens,
                "status": get_current_status()
            }

        current_daily_event = None
        current_day_index += 1
        passengers_checked_today = 0
        approved_humans = 0
        denied_humans = 0
        approved_aliens = 0
        denied_aliens = 0

        # game ends only after all 7 days / 21 passengers
        if passenger_index >= len(passengers):
            return {
                "game_finished": True,
                "ending": get_ending(),
                "status": get_current_status()
            }

        return {
            "day_finished": True,
            "show_event": False,
            "event": None,
            "approved_humans": summary_approved_humans,
            "denied_humans": summary_denied_humans,
            "approved_aliens": summary_approved_aliens,
            "denied_aliens": summary_denied_aliens,
            "status": get_current_status()
        }

    return {
        "day_finished": False,
        "next_passenger": get_current_passenger_full_data(),
        "approved_humans": approved_humans,
        "denied_humans": denied_humans,
        "approved_aliens": approved_aliens,
        "denied_aliens": denied_aliens
    }


def move_to_next_passenger():
    global passenger_index, passengers_checked_today, current_game_data
    passenger_index += 1
    passengers_checked_today += 1
    current_game_data = {}


def use_boost():
    passenger = passengers[passenger_index]

    if state["surprise_boost_days"] > 0:
        cursor.execute(
            "select surprise_factor from passenger where id=%s;",
            (passenger["id"],)
        )
        result = cursor.fetchone()

        state["surprise_boost_days"] -= 1  # consume boost

        return {
            "used": True,
            "surprise_factor": result["surprise_factor"],
            "remaining": state["surprise_boost_days"]
        }
    else:
        return {
            "used": False
        }
def create_daily_event():
    events = [
        {
            "name": "power_outage",
            "text": "A power fluctuation hits the airport energy supply.",
            "option1": "Spend $1500 to stabilize generators",
            "option2": "Do nothing and risk energy loss"
        },
        {
            "name": "government_audit",
            "text": "Government inspectors arrive unexpectedly.",
            "option1": "Pay $2000 to impress inspectors",
            "option2": "Risk reputation loss"
        },
        {
            "name": "staff_kidnap",
            "text": "Airport staff are held hostage by aliens.",
            "option1": "Pay ransom ($3000)",
            "option2": "Ignore them"
        },
        {
            "name": "passengers_flu",
            "text": "Passengers have been contaminated by an odd flu. The flu makes them laugh hysterically.",
            "option1": "Quarantine part of the airport",
            "option2": "Let them laugh until it passes"
        },
        {
            "name": "fire_in_the_hole",
            "text": "Some sectors of the airport caught fire.",
            "option1": "Ask the public for donations",
            "option2": "Pay and fix it yourself"
        }
    ]

    return random.choice(events)
def apply_daily_event_choice(choice):
    global state, current_daily_event
    global current_day_index, approved_humans, denied_humans, approved_aliens, denied_aliens, passengers_checked_today

    event_name = current_daily_event["name"]

    if event_name == "power_outage":
        if choice == "1":
            if state["budget"] >= 1500:
                state["budget"] -= 1500
                message = "Generators stabilized."
            else:
                message = "You cannot afford it."
        else:
            state["energy"] -= 20
            message = "Generators damaged. Energy lost."

    elif event_name == "government_audit":
        if choice == "1":
            state["budget"] -= 2000
            state["reputation"] += 10
            message = "Inspectors found no issues."
        else:
            state["reputation"] -= 15
            message = "The audit damaged public trust."

    elif event_name == "staff_kidnap":
        if choice == "1":
            state["budget"] -= 3000
            state["reputation"] += 5
            message = "The staff were rescued."
        else:
            state["reputation"] -= 25
            message = "The public is furious and you probably need a new employee."

    elif event_name == "passengers_flu":
        if choice == "1":
            state["budget"] -= 1000
            state["reputation"] += 10
            state["sustainability"] += 10
            message = "You quarantined part of the airport."
        else:
            state["reputation"] -= 10
            state["sustainability"] -= 10
            message = "Now everybody is laughing thanks to you! That would be great, if this was stand-up comedy."

    elif event_name == "fire_in_the_hole":
        if choice == "1":
            donations = random.randint(1, 1000)
            state["budget"] += donations

            if donations >= 500:
                state["budget"] -= 500
                message = "Donations were enough to control the fire."
            else:
                state["reputation"] -= 25
                state["sustainability"] -= 20
                message = "Nobody really cared about the funding you created, you gon lose some stats."
        else:
            state["budget"] -= 500
            message = "The fire has been controlled, no need for crying on TV."

    state = max_state(state)

    current_day_index += 1
    current_daily_event = None

    approved_humans = 0
    denied_humans = 0
    approved_aliens = 0
    denied_aliens = 0
    passengers_checked_today = 0

    if passenger_index >= len(passengers):
        return {
            "game_finished": True,
            "ending": get_ending(),
            "message": message,
            "status": get_current_status()
        }

    return {
        "game_finished": False,
        "message": message,
        "status": get_current_status()
    }
def create_backstabber_event():
    return {
        "text": "The strange passenger whispers: 'We're not all your enemy, you know?' There is a strange glow in their eyes, but it looks friendly.",
        "option1": "Hear them out",
        "option2": "Something's fishy..."
    }
def apply_backstabber_choice(choice, boost_choice=None):
    global state, denied_aliens

    if choice == "2":
        message = "You refusd their offer. They vanish into the crowd."
        denied_aliens +=1
        move_to_next_passenger()
        next_step = continue_after_passenger()
        next_step["message"] = message
        next_step["betrayed"] = False
        next_step["needs_boost_choice"] = False
        next_step["status"] = get_current_status()
        return next_step


    if boost_choice is None and False:
        stolen = state["budget"]
        state["budget"] = 0
        state["energy"] = max(0, state["energy"] - 50)
        state["reputation"] = max(0, state["reputation"] - 35)
        state = max_state(state)

        message = "They betrayed you. Your cash was stolen: " + str(stolen)
        move_to_next_passenger()
        next_step = continue_after_passenger()
        next_step["message"] = message
        next_step["betrayed"] = True
        next_step["needs_boost_choice"] = False
        next_step["status"] = get_current_status()
        return next_step

    if boost_choice is None:
        return {
            "message": "They offer you a boost. Choose one.",
            "betrayed": False,
            "needs_boost_choice": True,
            "boosts": [
                "Reveal surprise factors for the next 3 days",
                "Restore energy",
                "Restore reputation",
                "Boost sustainability",
                "Receive cash"
            ],
            "status": get_current_status()
        }

    if boost_choice == "1":
        state["surprise_boost_days"] = 3
        message = "Boost activated: surprise factors for 3 days."

    elif boost_choice == "2":
        restore = random.randint(10, 40)
        state["energy"] = min(100, state["energy"] + restore)
        message = "Energy restored by " + str(restore)

    elif boost_choice == "3":
        restore = random.randint(10, 30)
        state["reputation"] = min(100, state["reputation"] + restore)
        message = "Reputation restored by " + str(restore)

    elif boost_choice == "4":
        boost = random.randint(10, 30)
        state["sustainability"] = min(100, state["sustainability"] + boost)
        message = "Sustainability increased by " + str(boost)

    elif boost_choice == "5":
        cash = random.randint(100, 3000)
        state["budget"] += cash
        message = "You received " + str(cash) + " credits."

    else:
        message = "The passenger vanishes."

    state = max_state(state)
    denied_aliens += 1
    move_to_next_passenger()
    next_step = continue_after_passenger()
    next_step["message"] = message
    next_step["betrayed"] = False
    next_step["needs_boost_choice"] = False
    next_step["status"] = get_current_status()
    return next_step


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

def day_intro(day, state):
        return {
            "day": f"{day} DECEMBER",
            "energy": state["energy"],
            "budget": state["budget"],
            "reputation": state["reputation"],
            "reputation_emoji": reputation_emoji(state["reputation"]),
            "sustainability": state["sustainability"]
        }

def get_ending():
    if state["energy"] <= 0:
        return {
            "title": "GAME OVER",
            "message": "Out of energy. The airport shut down and the aliens took over."
        }

    if state["reputation"] <= 0:
        return {
            "title": "GAME OVER",
            "message": "People don't trust the airport anymore. The government cut funding."
        }

    if state["sustainability"] < 30 and state["budget"] <= 0:
        return {
            "title": "GAME OVER",
            "message": "The airport became unsustainable and lost government support."
        }

    if total_approved_aliens <= 2:
        return {
            "title": "YOU WON",
            "message": "You successfully protected Earth from the disguised aliens."
        }

    return {
        "title": "GAME OVER",
        "message": "Too many aliens passed through the airport."
    }



