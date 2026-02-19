from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types




planning_agent = LlmAgent(
    name='planning_agent',
    model='gemini-2.5-flash',
    planner = BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True, # Shows the agent's reasoning
            thinking_budget=1024 # Tokens reserved for thinking
        )
    ),
    instruction = "Solve complex ideas by reasoning"
)
root_agent = planning_agent


