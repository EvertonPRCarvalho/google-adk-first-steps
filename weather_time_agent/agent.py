import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from tools.get_time_zone import get_time_zone 
from tools.post_weather import post_weather
from tools.post_current_weather import post_current_weather
from interaction.call_agent_async import call_agent_async

# from google.cloud import aiplatform

# aiplatform.init(project="dauntless-theme-426901-r6", location="southamerica-east1")

# response = aiplatform.PredictionServiceClient().predict(...)


# --- Session Management ---
# Key Concept: SessionService stores conversation history & state.
# InMemorySessionService is simple, non-persistent storage for this tutorial.
session_service = InMemorySessionService()

# Define constants for identifying the interaction context
APP_NAME = "weather_time_agent"
USER_ID = "user_1"
SESSION_ID = "session_001" # Using a fixed ID for simplicity

# Create the specific session where the conversation will happen
session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
)
print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

# -- Configure Model--
AGENT_MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
AGENT_MODEL = AGENT_MODEL_GEMINI_2_0_FLASH

root_agent = Agent(
    name=APP_NAME,
    model=AGENT_MODEL,
    description=
        "Provides weather information for specific country.",
    instruction=
        "You are a helpful weather assistant. "
        "When the user asks for the weather in a specific country, "
        "use the 'get_time_zone' to get longitude and latitude to execute 'post_current_weather' tool to find the information. "
        "If the tool returns an error, inform the user politely. "
        "If the tool is successful, present the weather report clearly.",
    tools=[get_time_zone, post_current_weather]
)
print(f"Agent '{root_agent.name}' created using model '{AGENT_MODEL}'.")

# --- Runner ---
# Key Concept: Runner orchestrates the agent execution loop.
runner = Runner(
    agent=root_agent, # The agent we want to run
    app_name=APP_NAME,   # Associates runs with our app
    session_service=session_service # Uses our session manager
)

print(f"Runner created for agent '{runner.agent.name}'.")