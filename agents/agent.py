from google.adk.agents.llm_agent import Agent
from agents.sub_agents.clientcom_agent import clientcom_agent
from agents.prompt import ROOT_INSTR

# Controller agent
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Main conductor, directing clients to the right',
    instruction=ROOT_INSTR,
)

def handle_user_input(message: str):
    """Route the user’s input to the right agent"""
    if "client" in message.lower():
        return clientcom_agent.run(message)
    else:
        return root_agent.run(message)