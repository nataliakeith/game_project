import random


def daily_event(state):

    events = [
        power_outage,                                            #
        government_audit,
        staff_kidnap,
        system_malfunction
    ]

    event = random.choice(events)

    state = event(state)

    return state

def power_outage(state):

    print("\n--- DAILY EVENT ---")
    print("A power fluctuation hits the airports energy supply.")

    print("1) Spend $1500 to stabilize generators")
    print("2) Do nothing and risk energy loss")

    choice = input("Choose: ")

    if choice == "1":

        if state["budget"] >= 1500:
            state["budget"] -= 1500
            print("Generators stabilized.")

        else:
            print("You cannot afford it.")

    else:

        state["energy"] -= 20
        print("Generators damaged.Energy lost.")

    return state

#EVENT TWOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

def government_audit(state):

    print("\n--- DAILY EVENT ---")
    print("Government inspectors arrive unexpectedly.")

    print("1) Pay $2000 to impress inspectors")
    print("2) Risk reputation loss")

    choice = input("Choose: ")

    if choice == "1":

        state["budget"] -= 2000
        state["reputation"] += 10
        print("Inspectors don't see any issues with the airport.")

    else:

        state["reputation"] -= 15
        print("The audit report damages public trust.")

    return state

#EVENT THREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE

def staff_kidnap(state):

    print("\n--- DAILY EVENT ---")
    print("Airport staff held hostage by aliens.")

    print("1) Pay ransom ($3000)")
    print("2) Ignore them")

    choice = input("Choose: ")

    if choice == "1":

        state["budget"] -= 3000
        state["reputation"] += 5

    else:

        state["reputation"] -= 25

    return state

#EVENT FOURRRRRRRR

def system_malfunction(state):

    print("\n--- DAILY EVENT ---")
    print("Passport scanners malfunction today.")

    print("You cannot check passenger tickets today.")

    state["inspection_blocked"] = True

    return state