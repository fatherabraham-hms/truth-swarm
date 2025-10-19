import os
from pathlib import Path
from uagents import Agent, Context, Model
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Get seed phrase from environment variable
SEED_PHRASE = os.getenv("DEFI_AGENT_SEED_PHRASE")
if not SEED_PHRASE:
    raise ValueError("DEFI_AGENT_SEED_PHRASE environment variable not set")


agent = Agent(name="defi-agent",
              seed=SEED_PHRASE,
              port=8001,
              mailbox=True,
              readme_path="README.md"
              )
 
class AIRequest(Model):
    question: str

class AIResponse(Model):
    msg: str
    
    class Config:
        schema_extra = {
            "description": "Text response for truth swarm agent"
        }
 
@agent.on_event("startup")
async def state_metadata(ctx: Context):
    #log the agent name and address
    ctx.logger.info(f"Agent name: {agent.name}")
    ctx.logger.info(f"Agent address: {agent.address}")
    ctx.logger.info(
        f"Defi agent is running"
    ) 
 
@agent.on_message(model=AIRequest, replies={AIResponse})
async def handle_data(ctx: Context, sender: str, data: AIRequest):
    ctx.logger.info(f"Sender: {sender}")
    ctx.logger.info(f"Got message from AI agent: {data.question}")
    # Send response back to evaluator agent using its local endpoint
    await ctx.send(
        destination=sender, 
        message=AIResponse(msg="Eth is the most undervalued token on the market")
    )
 
agent.run()