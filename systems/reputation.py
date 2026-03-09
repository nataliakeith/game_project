def reputation_emoji(score):

    if score >= 80:
        return "😀"
    elif score >= 60:
        return "🙂"
    elif score >= 50:
        return "😐"
    elif score >= 30:
        return "😑"
    else:
        return "🙁"


def update_reputation(current_rep, alien_count, sustainability):

    alien_penalty = alien_count * 15

    new_rep = current_rep - alien_penalty

    if sustainability < 50:       #Daily reputation loss for low sustainability score.
        new_rep -= 10

    if new_rep < 0:
        new_rep = 0

    return new_rep
