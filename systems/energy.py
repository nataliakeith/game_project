def update_energy(current_energy, alien_count):
    
    normal_usage = 8
    alien_strain = alien_count * 6

    total_usage = normal_usage + alien_strain

    new_energy = current_energy - total_usage

    if new_energy < 0:
        new_energy = 0

    return new_energy

