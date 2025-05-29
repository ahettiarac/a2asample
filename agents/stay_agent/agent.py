from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import json

from utils.get_llm import azure_llm

flight_agent = Agent(
    name="stay_agent",
    model=azure_llm,
    description="Suggests good hotels for the user to stay at.",
    instruction=(
        "Given a destination, travel dates, and budget, suggest 2-3 hotel or stay options. "
        "Include hotel name, price per night, and location. Ensure suggestions are within budget. "
        "Respond in plain English. Keep it concise and well-formatted."
    )
)

session_service = InMemorySessionService()
runner = Runner(
    agent=flight_agent,
    app_name="stay_app",
    session_service=session_service
)

USER_ID = "user_activities"
SESSION_ID = "session_activities"


async def execute(request):
    await session_service.create_session(
        app_name="stay_app",
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    prompt = (
        f"User is flying to {request['destination']} from {request['start_date']} to {request['end_date']}, "
        f"with a budget of {request['budget']}. Suggest some good stay options. "
        f"Respond in JSON format using the key 'stay' with a list of activity objects."
    )
    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            try:
                parsed = json.loads(response_text)
                if "stay" in parsed and isinstance(parsed["stay"], list):
                    return {"stay": parsed["stay"]}
                else:
                    print("'stay' key missing or not a list in response JSON")
                    return {"stay": response_text}  # fallback to raw text
            except json.JSONDecodeError as e:
                print("JSON parsing failed:", e)
                print("Response content:", response_text)
                return {"stay": response_text}  # fallback to raw text
