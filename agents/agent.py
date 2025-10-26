from google.adk.agents import Agent
from .sub_agents.agent import clientcom_agent
from .prompt import INSURANCE_INSTR
from .prompt import ROOT_INSTR
from .prompt import PERSONAL_INJURY_INSTR
from google.adk.tools import AgentTool

# Controller agent
# root_agent = Agent(
#     model='gemini-2.5-flash',
#     name='root_agent',
#     description='Main conductor, directing clients to the right',
#     instruction=ROOT_INSTR,
#     sub_agents=[
#         clientcom_agent
#     ]
# )

# Insurance Agent
insurance_agent = Agent(
    model='gemini-2.5-flash',
    name='insurance_agent',
    description='Handles insurance related claims',
    instruction=INSURANCE_INSTR,
    
)

# Personal Injury Protection Agent
injury_agent = Agent(
    model='gemini-2.5-flash',
    name='injury_agent',
    description='Handles injury claim',
    instruction=PERSONAL_INJURY_INSTR,
    
)



# Root agent
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Main conductor, directing clients to the right',
    instruction=ROOT_INSTR,
    
    tools=[
        AgentTool(agent=insurance_agent),
        AgentTool(agent=injury_agent),
    ]
)




