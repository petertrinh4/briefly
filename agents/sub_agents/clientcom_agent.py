from google.adk.agents.llm_agent import Agent
from agents.prompt import CLIENTCOM_INSTR

# Purpose: polish the user input/demands to format into an email/msg
clientcom_agent = Agent(
    model='gemini-2.5-flash',
    name='clientcom_agent',
    description='Drafts clear, empathetic messages to clients and acts as the gatekeeper before sending.',
    instruction=CLIENTCOM_INSTR,
)
