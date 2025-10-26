from google.adk.agents import Agent
from .prompt import CLIENTCOM_INSTR # -> Same folder
from agents.gmail import gmail_send
from google.adk.tools import FunctionTool

#gmail_tool = FunctionTool(func=gmail_send, name="gmail_send")

# Purpose: polish the user input/demands to format into an email/msg
clientcom_agent = Agent(
    model='gemini-2.5-flash',
    name='clientcom_agent',
    description='Drafts clear, empathetic messages to clients and acts as the gatekeeper before sending.',
    instruction=CLIENTCOM_INSTR,
   # tools=[gmail_tool],
)
