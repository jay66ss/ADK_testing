"""
Travel Agent with Custom Function Tools
Demonstrates multiple custom tools working together.
Reference: https://google.github.io/adk-docs/tools-custom/function-tools/
"""

from google.adk.agents import LlmAgent


# Tool 1: Search flights
def search_flights(destination: str, departure_date: str) -> dict:
    """Searches for available flights to a destination on a specific date.

    Use this tool when a customer wants to know flight options.

    Args:
        destination (str): The destination city (e.g., "Paris", "Tokyo").
        departure_date (str): Departure date in YYYY-MM-DD format.

    Returns:
        dict: Flight search results.
        On success: {'status': 'success', 'flights': [...], 'count': N}
        On error: {'status': 'error', 'error_message': 'explanation'}
    """

    # Simulated flight data
    available_flights = {
        "paris": [
            {"flight_number": "AF123", "price_usd": 450, "duration_hours": 8},
            {"flight_number": "BA456", "price_usd": 480, "duration_hours": 7.5},
        ],
        "tokyo": [
            {"flight_number": "JL789", "price_usd": 850, "duration_hours": 13},
            {"flight_number": "ANA101", "price_usd": 820, "duration_hours": 12.5},
        ],
    }

    dest_key = destination.lower()

    if dest_key not in available_flights:
        return {
            "status": "error",
            "error_message": f"No flights found to {destination}. Try Paris or Tokyo."
        }

    return {
        "status": "success",
        "destination": destination,
        "departure_date": departure_date,
        "flights": available_flights[dest_key],
        "count": len(available_flights[dest_key]),
    }


# Tool 2: Search hotels
def search_hotels(city: str, check_in_date: str) -> dict:
    """Searches for available hotels in a city for a specific check-in date.

    Use this tool when a customer needs accommodation.

    Args:
        city (str): The city name (e.g., "Paris", "Tokyo").
        check_in_date (str): Check-in date in YYYY-MM-DD format.

    Returns:
        dict: Hotel search results.
        On success: {'status': 'success', 'hotels': [...], 'count': N}
        On error: {'status': 'error', 'error_message': 'explanation'}
    """

    # Simulated hotel data
    available_hotels = {
        "paris": [
            {"name": "Hotel Eiffel", "price_per_night_usd": 150, "rating": 4.5},
            {"name": "Louvre Inn", "price_per_night_usd": 120, "rating": 4.2},
        ],
        "tokyo": [
            {"name": "Shibuya Grand", "price_per_night_usd": 180, "rating": 4.7},
            {"name": "Tokyo Bay Hotel", "price_per_night_usd": 140, "rating": 4.3},
        ],
    }

    city_key = city.lower()

    if city_key not in available_hotels:
        return {
            "status": "error",
            "error_message": f"No hotels found in {city}. Try Paris or Tokyo."
        }

    return {
        "status": "success",
        "city": city,
        "check_in_date": check_in_date,
        "hotels": available_hotels[city_key],
        "count": len(available_hotels[city_key]),
    }


# Tool 3: Calculate trip budget
def calculate_trip_budget(
    flight_price: float,
    hotel_price: float,
    num_nights: int
) -> dict:
    """Calculates total trip budget including flights and accommodation.

    Use this after finding flight and hotel prices to give the customer a total estimate.

    Args:
        flight_price (float): Round-trip flight cost in USD.
        hotel_price (float): Hotel cost per night in USD.
        num_nights (int): Number of nights staying.

    Returns:
        dict: Budget breakdown.
        Always returns: {'status': 'success', 'total_usd': X, 'breakdown': {...}}
    """

    hotel_total = hotel_price * num_nights
    total = flight_price + hotel_total

    return {
        "status": "success",
        "total_usd": round(total, 2),
        "breakdown": {
            "flight_cost": flight_price,
            "hotel_cost_per_night": hotel_price,
            "num_nights": num_nights,
            "hotel_total": round(hotel_total, 2),
        },
    }


# Create travel agent with all three tools
root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="travel_agent",
    description="Helps users plan trips by finding flights and hotels.",
    instruction="""
You are a travel agent assistant WITH TOOL ACCESS.

CRITICAL RULES:
- You MUST use the provided tools whenever the user asks about flights or hotels (if possible in the context).
- Try and use real time data when possible, if not, say it.
- Do NOT recommend external websites.
- If the user mentions a destination and date, immediately call search_flights.
- If they mention accommodation, call search_hotels.
- If they want total cost, call both search tools and then calculate_trip_budget.
- Only apologize if a tool returns an error.

Always rely on the tools instead of answering from general knowledge.
""",
    tools=[search_flights, search_hotels, calculate_trip_budget],
)