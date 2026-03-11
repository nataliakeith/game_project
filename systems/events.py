import random


def daily_event(state):

    events = [
        power_outage,                                            #
        government_audit,
        staff_kidnap,
        system_malfunction,
        passengers_flu,
        fire_in_the_hole,
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

#EEVENT FIVEEEEEEEE

def passengers_flu(state):
    print("\n--- DAILY EVENT ---")
    print("Passengers have being contaminated by a odd flu.")
    print("The flu makes them laugh hysterically.")
    print("1) Quarantine some areas of the airport, to stop the spreading")
    print("2) Let them laugh until it passes")

    choice = input("Choose: ")

    if choice == "1":
        print("You quarantined part of the airport.")
        state["budget"] -= 1000
        state["reputation"] += 10
        state["sustainability"] += 10

    else:
        print("Now everybody is laughing thanks to you!")
        print("That would be great, if this was stand-up comedy.")

        state["reputation"] -= 10
        state["sustainability"] -= 10

    return state


#EVENT SIXXXXX

def fire_in_the_hole(state):
    print("Some sectors in the Airport caught fire.")
    print("1) You can appeal to the public and get donations creating a funding.")
    print("2) You can pay and fix it yourself.")

    choice= input("Choose: ")

    if choice == "1":
        donations = random.randint(1, 1000)
        state["budget"] += donations
        if donations >= 500:
            print("You have gotten enough donations to control the fire and fix the airport")
            state["budget"] -= 500
        if donations < 500:
            print("Nobody really cared about the funding you created, I guess all that crying wasn't enough")
            state["reputation"] -= 25
            state["sustainability"] -= 20
    else:
        print("The fire has been controlled, no need for crying on TV.")
        state["budget"] -= 500

    return state







