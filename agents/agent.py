from google.adk.agents import Agent
from .prompt import ROOT_INSTR
from .sub_agents.clientcom.agent import clientcom_agent

# Controller agent
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Main conductor, directing clients to the right',
    instruction=ROOT_INSTR,
    sub_agents=[
        clientcom_agent
    ]
)