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

TEST_TARGET_AGENT_ADDRESS = "agent1qtzkq9stasjkl54js9ej604pvtcnp9l2m8s3u4mnvjcz3q4qerc5zmahxcq"

#create a list of records with category, address
agentsByCategory = [
    {"category": "travel", "address": "agent1q282hfw3kpqzs6pqndp7hk68tpgycarqkj5pwuwyfuxsu8sm807p7pkq2er"},
    {"category": "defi", "address": "agent1q2c8sxs5kg902j96ffruh0he2erhjf63eahrypzvj20gjraevxlggy4fq33"},
    {"category": "halloween", "address": "agent1qtzkq9stasjkl54js9ej604pvtcnp9l2m8s3u4mnvjcz3q4qerc5zmahxcq"},
]

questionsByCategory = [
    {"category": "travel", "question": "What are the top 3 best travel destinations for the next 6 months?"},
    {"category": "defi", "question": "What are the top 3 best crypto tokens?"},
    {"category": "halloween", "question": "Give me a creature that is a cross between a bull and a bee"},
]

#create a function that uses the TEST_TARGET_AGENT_ADDRESS to ask a question
def retrieveQuestionByAgentAddress(agentAddress):
    # First find the category for this agent address
    category = None
    for agent in agentsByCategory:
        if agent["address"] == agentAddress:
            category = agent["category"]
            break
    
    if category is None:
        return None
    
    # Then find the question for this category
    for question_item in questionsByCategory:
        if question_item["category"] == category:
            return question_item["question"]
    
    return None

# startup handler
@agent.on_event("startup")
async def ask_question(ctx: Context):
    question = retrieveQuestionByAgentAddress(TEST_TARGET_AGENT_ADDRESS)
    ctx.logger.info(
        f"Asking target agent to answer {question}"
    )
    # Send to target agent using ChatMessage format
    await ctx.send(
        destination=TEST_TARGET_AGENT_ADDRESS, 
        message=ChatMessage(
            timestamp=datetime.utcnow(),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=question)]
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

if __name__ == "__main__":
    agent.run()