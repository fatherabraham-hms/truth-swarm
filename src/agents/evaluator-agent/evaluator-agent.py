import os
from pathlib import Path
from dotenv import load_dotenv
from uagents import Agent, Context, Model
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    TextContent,
    chat_protocol_spec,
)
from datetime import datetime
from uuid import uuid4
import random

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Get seed phrase from environment variable
SEED_PHRASE = os.getenv("TRUTH_SWARM_AGENT_SEED_PHRASE")
if not SEED_PHRASE:
    raise ValueError("TRUTH_SWARM_AGENT_SEED_PHRASE environment variable not set")

# Instantiate agent agent1qtak6m7rgytst3zqmu744t0k8z4xytf3zrnct49efqvwxzqc3f3t5rkflj4
agent = Agent(
    name="truthswarm",
    seed=SEED_PHRASE,
    port=8000,
    mailbox=True,
    readme_path="README.md"
)

QUESTION = "What are the top 3 best travel destinations for the next 6 months?"

# startup handler
@agent.on_event("startup")
async def ask_question(ctx: Context):
    ctx.logger.info(
        f"Asking target agent to answer {QUESTION}"
    )
    # Send to target agent using ChatMessage format
    await ctx.send(
        destination='agent1q282hfw3kpqzs6pqndp7hk68tpgycarqkj5pwuwyfuxsu8sm807p7pkq2er', 
        message=ChatMessage(
            timestamp=datetime.utcnow(),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=QUESTION)]
        )
    )

class AIRequest(Model):
    question: str
class AIResponse(Model):
    text: str
    
    class Config:
        schema_extra = {
            "description": "Text response for truth swarm agent"
        }

# Handler for receiving responses from other agents
@agent.on_message(model=ChatMessage)
async def handle_ai_response(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"Received response from {sender}: {msg.text}")
    # randomly return either "evaluated as good" or "evaluated as bad"
    result = "Evaluated as good" if random.random() > 0.5 else "Evaluated as bad"
    #log agent address and result
    ctx.logger.info(f"Agent {sender} response evaluated as: {result}")

# Handler for evaluating questions (if this agent receives questions)
@agent.on_message(model=AIRequest, replies={AIResponse})
async def do_evaluation(ctx: Context, sender: str, msg: AIRequest):
    ctx.logger.info(f"Received question from {sender}: {msg.question}")
    # randomly return either "evaluated as good" or "evaluated as bad"
    result = "Evaluated as good" if random.random() > 0.5 else "Evaluated as bad"
    #log agent address and result
    ctx.logger.info(f"Agent {sender} evaluated {msg.question} as {result}")

    message = AIResponse(text="Thanks for your response")
    await ctx.send(
        destination=sender, 
        message=message
    )


# @agent.on_message(model=Request)
# async def handle_message(ctx: Context, sender: str, msg: Request):
#     """Log the received message and reply to the sender"""
#     ctx.logger.info(f"Received message from {sender}: {msg.message}")

#     if sender == 'agent1q0r8wgtnxqwegudp5k3cmf4hnu44q6y997fdg3pz8c3exhw04vu3yy4wdwd':
#         await ctx.send(sender, Request(message="hello there alice"))
#     elif sender == 'agent1q282hfw3kpqzs6pqndp7hk68tpgycarqkj5pwuwyfuxsu8sm807p7pkq2er':
#         await ctx.send(sender, Request(message="Hello there Travel Agent!"))
#     else:
#         await ctx.send(sender, Request(message="hello there friend"))

if __name__ == "__main__":
    agent.run()