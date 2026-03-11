def update_sustainability(current_value, alien_count):

    waste_penalty = alien_count * 15

    new_value = current_value - waste_penalty

    if new_value < 0:
        new_value = 0

    return new_value