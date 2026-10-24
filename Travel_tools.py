
"""BudgetWise Travel Planner cost and transport tools."""

TRANSPORT_DATA = {
    "Delhi-Jaipur": [
        {"type": "Train", "cost": 450, "hours": 4.5},
        {"type": "Bus", "cost": 500, "hours": 5},
        {"type": "Flight", "cost": 3500, "hours": 1},
    ],
    "Delhi-Agra": [
        {"type": "Train", "cost": 250, "hours": 2},
        {"type": "Bus", "cost": 350, "hours": 3},
    ],
    "Delhi-Rishikesh": [
        {"type": "Train", "cost": 350, "hours": 5},
        {"type": "Bus", "cost": 500, "hours": 6},
    ],
    "Delhi-Haridwar": [
        {"type": "Train", "cost": 300, "hours": 4},
        {"type": "Bus", "cost": 400, "hours": 5},
    ],
}

HOTEL_DATA = {
    "Jaipur": 700,
    "Agra": 600,
    "Rishikesh": 700,
    "Haridwar": 600,
}

FOOD_ACTIVITY_DATA = {
    "Jaipur": {"food": 500, "activities": 800},
    "Agra": {"food": 450, "activities": 600},
    "Rishikesh": {"food": 500, "activities": 700},
    "Haridwar": {"food": 450, "activities": 500},
}


def get_travel_options(origin, destination):
    """Return available transport options for a supported route."""
    origin = origin.strip().title()
    destination = destination.strip().title()

    route = f"{origin}-{destination}"
    options = TRANSPORT_DATA.get(route)

    if options is not None:
        return options

    reverse_route = f"{destination}-{origin}"
    reverse_options = TRANSPORT_DATA.get(reverse_route)

    if reverse_options is not None:
        return reverse_options

    return []


def get_destination_costs(destination):
    """Return estimated destination costs."""
    destination = destination.strip().title()
    hotel = HOTEL_DATA.get(destination)
    food_activity = FOOD_ACTIVITY_DATA.get(destination)

    if hotel is None or food_activity is None:
        return None

    return {
        "hotel": hotel,
        "food": food_activity["food"],
        "activities": food_activity["activities"],
    }


def calculate_trip_cost(
    budget,
    travellers,
    days,
    transport_per_person,
    hotel_per_night,
    food_per_person_per_day,
    activities_per_person,
):
    """Calculate estimated round-trip costs for a shared hotel room."""
    if budget < 0 or travellers < 1 or days < 1:
        raise ValueError("Budget must be non-negative; travellers and days must be positive.")

    transport = transport_per_person * travellers * 2
    hotel = hotel_per_night * max(days - 1, 0)
    food = food_per_person_per_day * travellers * days
    activities = activities_per_person * travellers

    total = transport + hotel + food + activities
    remaining = budget - total

    return {
        "transport": transport,
        "hotel": hotel,
        "food": food,
        "activities": activities,
        "total": total,
        "remaining": remaining,
        "within_budget": remaining >= 0,
    }
