import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from tools.get_time_zone import get_time_zone 
from tools.post_weather import post_weather
from tools.post_current_weather import post_current_weather
from interaction.call_agent_async import call_agent_async
from weather_time_agent_2.greeting_agent import greeting_agent
from weather_time_agent_2.farewell_agent import farewell_agent
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

if(greeting_agent and farewell_agent and 'get_time_zone' in globals() and 'post_current_weather' in globals()):
    print("All tools and agents are defined correctly.")
    root_agent = Agent(
        name=APP_NAME,
        model=AGENT_MODEL,
        description=
            "The main coordinator agent. Handles weather requests and delegates greetings/farewells to specialists.",
        instruction=
            "You are the main Weather Agent coordinating a team. Your primary responsibility is to provide weather information. "
            "Use the 'get_time_zone' tool ONLY for specific weather requests (e.g., 'weather in London'). "
            "use the 'get_time_zone' to get longitude and latitude to execute 'post_current_weather' tool to find the information. "
            "You are a helpful weather assistant. "
            "You have specialized sub-agents: "
            "1. 'greeting_agent': Handles simple greetings like 'Hi', 'Hello'. Delegate to it for these. "
            "2. 'farewell_agent': Handles simple farewells like 'Bye', 'See you'. Delegate to it for these. "
            "Analyze the user's query. If it's a greeting, delegate to 'greeting_agent'. If it's a farewell, delegate to 'farewell_agent'. "
            "If it's a weather request, handle it yourself using 'get_weather'. "
            "For anything else, respond appropriately or state you cannot handle it."
            "When the user asks for the weather in a specific country, "
            "If the tool returns an error, inform the user politely. "
            "If the tool is successful, present the weather report clearly.",
        tools=[get_time_zone, post_current_weather],
        sub_agents=[greeting_agent, farewell_agent]
        )
    print(f"✅ Root Agent '{root_agent.name}' created using model '{root_agent.model}' with sub-agents: {[sa.name for sa in root_agent.sub_agents]}")

else:
    print("❌ Cannot create root agent because one or more sub-agents failed to initialize or 'get_weather' tool is missing.")
    if not greeting_agent: print(" - Greeting Agent is missing.")
    if not farewell_agent: print(" - Farewell Agent is missing.")
    if 'get_weather' not in globals(): print(" - get_weather function is missing.")

# --- Runner ---
# Key Concept: Runner orchestrates the agent execution loop.
runner = Runner(
    agent=root_agent, # The agent we want to run
    app_name=APP_NAME,   # Associates runs with our app
    session_service=session_service # Uses our session manager
)

print(f"Runner created for agent '{runner.agent.name}'.")