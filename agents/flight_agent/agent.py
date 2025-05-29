from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import json

from utils.get_llm import azure_llm

flight_agent = Agent(
    name="flight_agent",
    model=azure_llm,
    description="Suggests flight options for a destination.",
    instruction=(
        "Given a destination, travel dates, and budget, suggest 1-2 realistic flight options. "
        "Include airline name, price, and departure time. Ensure flights fit within the budget."
    )
)

session_service = InMemorySessionService()
runner = Runner(
    agent=flight_agent,
    app_name="flight_app",
    session_service=session_service
)

USER_ID = "user_activities"
SESSION_ID = "session_activities"


async def execute(request):
    await session_service.create_session(
        app_name="flight_app",
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    prompt = (
        f"User is flying from {request['origin']} to {request['destination']} "
        f"from {request['start_date']} to {request['end_date']}, with a budget of {request['budget']}. "
        "Suggest 2-3 realistic flight options. For each option, include airline, departure time, return time, "
        "price, and mention if it's direct or has layovers."
        f"Respond in JSON format using the key 'flight' with a list of activity objects."
    )
    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            try:
                parsed = json.loads(response_text)
                if "flight" in parsed and isinstance(parsed["flight"], list):
                    return {"flight": parsed["flight"]}
                else:
                    print("'flights' key missing or not a list in response JSON")
                    return {"flights": response_text}  # fallback to raw text
            except json.JSONDecodeError as e:
                print("JSON parsing failed:", e)
                print("Response content:", response_text)
                return {"flights": response_text}  # fallback to raw text
