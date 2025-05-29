from common.a2aclient import call_agent

FLIGHT_URL = "http://localhost:8001/run"
STAY_URL = "http://localhost:8002/run"
ACTIVITIES_URL = "http://localhost:8003/run"


async def run(payload):
    print("Incoming payload:", payload)
    flights = await call_agent(FLIGHT_URL, payload)
    stay = await call_agent(STAY_URL, payload)
    activities = await call_agent(ACTIVITIES_URL, payload)

    print("flights:", flights)
    print("stay:", stay)
    print("activities:", activities)

    flights = flights if isinstance(flights, dict) else {}
    stay = stay if isinstance(stay, dict) else {}
    activities = activities if isinstance(activities, dict) else {}

    return {
        "flights": flights.get("flights", "No flights returned."),
        "stay": stay.get("stays", "No stay options returned."),
        "activities": activities.get("activities", "No activities found.")
    }
