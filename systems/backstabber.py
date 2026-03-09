import random


def check_backstabber():
    
    #Small chance that an alien is a backstabber merchant.Maybe too small?We'll see!
    
    chance = 0.2  # 20% chance (We can change as we go!)

    return random.random() < chance


def backstab(state):
    "Backstabber appears and offers boosts."

    print("\n================================")
    print("The strange passenger whispers to you...")
    print("'We're not all your enemy you know?...'")
    print("There's a strange glow in their eyes but it looks friendly.They offer to help you.")
    print("================================\n")

    print("Do you trust the strange passenger?")
    print("1 - Hear them out")
    print("2 - Something's fishy...")

    choice = input("Choose 1 or 2: ")   

    if choice == "2":
        print("You refused their offer.")
        print("They scoff at you.'Your loss.Don't say I didn't try to help you.'")
        return state, False                               # If we don't trust,it doesn't affect the game state

        # rare betrayal chance 15% for now.We can change as we go
    if random.random() < 0.15:

        print("\nThe passenger smiles strangely...")
        print('"Were humans always this gullible?"')
        print("Everything goes black.")
        print("You wake up hours later.The airport is in chaos.")

        stolen = state["budget"]
        state["budget"] = 0

        state["energy"] = max(0, state["energy"] - 50)
        state["reputation"] = max(0, state["reputation"] - 35)

        print("Your cash has been stolen:", stolen)
        print("Energy severely drained.")
        print("Reputation damaged.")

        print("While you were unconscious, the remaining passengers passed freely...")

        return state, True   # True means the day should end and state should be updated
    
    print("\n'Trust is a fragile thing nowadays friend.I appreciate this.'")

    print("Choose your boost:")
    print("1 - Reveal surprise factors for the next 3 days")
    print("2 - Restore energy")
    print("3 - Restore reputation")
    print("4 - Boost sustainability")
    print("5 - Receive cash")

    choice = input("Choose 1-5: ")

    if choice == "1":

        state["surprise_boost_days"] = 3
        print("Boost activated: You can check surprise factors for 3 days.")

    elif choice == "2":

        restore = random.randint(10, 40)
        state["energy"] = min(100, state["energy"] + restore)

        print("Energy restored by", restore)

    elif choice == "3":

        restore = random.randint(10, 30)
        state["reputation"] = min(100, state["reputation"] + restore)

        print("Reputation restored by", restore)

    elif choice == "4":

        if random.random() < 0.1:
            state["sustainability"] = 100
            print("You're one lucky fella! Sustainability maxed out!")
            print("Now those corporate drones won't bother you friend.")
        else:
            boost = random.randint(10, 30)
            state["sustainability"] = min(
                100, state["sustainability"] + boost)

            print("Sustainability increased by", boost)

    elif choice == "5":

        cash = random.randint(100, 3000)
        state["budget"] += cash

        print("You received", cash, "credits.")

    else:

        print("The strange passenger vanishes without a word.")

    return state, False  # The backstabber alien didn't betray us.The game continues normally