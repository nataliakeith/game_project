def update_budget(current_budget, reputation, sustainability):

    daily_cost = 1000
    funding = 0

    if reputation >= 40:
        funding = 2000
    else:
        funding = 1500   # Less 500 for low reputation

    new_budget = current_budget + funding - daily_cost

    if sustainability < 30:
        new_budget = 0

    return new_budget