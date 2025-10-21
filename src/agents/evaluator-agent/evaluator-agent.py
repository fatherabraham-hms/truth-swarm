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
from openai import OpenAI
from datetime import datetime
from uuid import uuid4
import random
import re

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Get seed phrase from environment variable
SEED_PHRASE = os.getenv("TRUTH_SWARM_AGENT_SEED_PHRASE")
if not SEED_PHRASE:
    raise ValueError("TRUTH_SWARM_AGENT_SEED_PHRASE environment variable not set")

# Instantiate agent agent1qtak6m7rgytst3zqmu744t0k8z4xytf3zrnct49efqvwxzqc3f3t5rkflj4
eval_comms_agent = Agent(
    name="truthswarm",
    seed=SEED_PHRASE,
    port=8000,
    mailbox=True,
    readme_path="README.md"
)

TEST_TARGET_AGENT_ADDRESS = "agent1q282hfw3kpqzs6pqndp7hk68tpgycarqkj5pwuwyfuxsu8sm807p7pkq2er"

EVAL_CATEGORIES = [
    "correctness",
    "capabilities",
    "domainKnowledge",
    "speed"
]

agentsByCategory = [
    {"category": "travel", "address": "agent1q282hfw3kpqzs6pqndp7hk68tpgycarqkj5pwuwyfuxsu8sm807p7pkq2er", "wallet": "fetch1lpwf86sdz3wcs2xvx5wjl7c3vzewt8q42d24wx"},
    {"category": "defi", "address": "agent1q2c8sxs5kg902j96ffruh0he2erhjf63eahrypzvj20gjraevxlggy4fq33", "wallet": "fetch1u4tnce3wsldqgp4ws5vesey60aq82k5ln8czn7"},
    {"category": "halloween", "address": "agent1qtzkq9stasjkl54js9ej604pvtcnp9l2m8s3u4mnvjcz3q4qerc5zmahxcq", "wallet": "fetch1zptj47xfa6kh7wyvtt3eem72p8r7547ygmuwa7"},
]

dataSetsByCategory = [
    {"category": "travel",
    "evalData": [
        {
            "id": "travel-1",
            "prompt": "What are the top 3 most popular travel destinations in Argentina in 2025?",
            "expected": "Buenos Aires, Iguaza Falls, Patagonia"
        }]},
    {"category": "defi", "evalData":
    [
        {
            "id": "defi-1",
            "prompt": "What are the top 3 best performing crypto tokens in 2025?",
            "expected": "Solana, XRP, Bitcoin"
        },
    ]},
    {"category": "halloween", "evalData":
    [
        {
            "id": "halloween-1",
            "prompt": "Give me a creature that is a cross between a bull and a bee",
            "expected": "Bull Bee"
        },
    ]},
]

# STATE MANAGEMENT CLASS
class EvalState:
    def __init__(self):
        self.currentQuestionId = ""
        self.currentCategory = ""
        self.currentEvalData = None
        self.currentResponse = ""
        self.evalResults = {}
        self.agent = None
    
    def set_current_question(self, question_id, category):
        self.currentQuestionId = question_id
        self.currentCategory = category

    def set_current_eval_data(self, eval_data):
        self.currentEvalData = eval_data

    def add_reponse(self, response):
        self.currentResponse = response
    
    def add_eval_result(self, correctness, capabilities, domainKnowledge, speed):
        self.evalResults = {
                "correctness": correctness,
                "capabilities": capabilities,
                "domainKnowledge": domainKnowledge,
                "speed": speed
        }

# Global state instance
eval_state = EvalState()

################# EVALUATOR AGENT #################
subject_matter = ("Return ONLY valid JSON matching the provided schema. You are an evaluator agent that evaluates the performance of other agents in a game."
"You evaluate the agent's responses and provide a rating for each category by evaluating the input json expected key.")

client = OpenAI(
    # By default, we are using the ASI-1 LLM endpoint and model
    base_url='https://api.asi1.ai/v1',

    # You can get an ASI-1 api key by creating an account at https://asi1.ai/dashboard/api-keys
    api_key=os.getenv("ASI1_API_KEY"),
)

def run_evaluator_agent(eval_data, tested_agent_response):
    response = 'I am afraid something went wrong and I am unable to answer your question at the moment'
    
    if not eval_data or not tested_agent_response:
        print("No eval data or tested agent response")
    
    print("Running test scoring...")
    try:
        r = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": f"""
        {subject_matter}. If the user asks 
        about any other topics, you should politely say that you do not know about them.
                """},
                {"role": "user", "content": eval_data},
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "type": "object",
                    "properties": {
                        "correctness": {"type": "number"},
                        "capabilities": {"type": "number"},
                        "domainKnowledge": {"type": "number"},
                        "speed": {"type": "number"}
                    },
                    "required": ["correctness", "capabilities", "domainKnowledge", "speed"]
                }
            },
            temperature=0.1,
            stream=false,
            max_tokens=2048,
        )

        response = str(r.choices[0].message.content)
    except:
        print('Error querying model')
    return response


################# UTIITY FUNCTIONS #################

def retrieveCategoryByAgentAddress(agentAddress):
    category = None
    for agent in agentsByCategory:
        if agent["address"] == agentAddress:
            category = agent["category"]
            break
    
    if category is None:
        return None
    
    return category
 
def retrievePromptsByCategory(category):    
    for eval_data in dataSetsByCategory:
        if eval_data["category"] == category:
            return eval_data["evalData"]
    
    return None
    

################# AGENTVERSE HANDLERS #################
@eval_comms_agent.on_event("startup")
async def init_eval(ctx: Context):
    category = retrieveCategoryByAgentAddress(TEST_TARGET_AGENT_ADDRESS)
    evalData = retrievePromptsByCategory(category)
    eval_state.set_current_eval_data(evalData)
    
    if not evalData:
        ctx.logger.error(f"No eval data found for category: {category}")
        return
    
    ctx.logger.info(
        f"Eval started for.. {category} on {TEST_TARGET_AGENT_ADDRESS}"
    )
    
    # Set current question in state
    eval_state.set_current_question(evalData[0]["id"], category)
    ctx.logger.info(f"Set currentQuestionId to: {eval_state.currentQuestionId}")
    
    # Send to target agent using ChatMessage format
    await ctx.send(
        destination=TEST_TARGET_AGENT_ADDRESS, 
        message=ChatMessage(
            timestamp=datetime.now(),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=evalData[0]["prompt"])]
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

########## AGENT TO AGENT HANDLERS ##########
@eval_comms_agent.on_message(model=ChatMessage)
async def handle_ai_response(ctx: Context, sender: str, msg: ChatMessage):
    # Extract text content from ChatMessage
    target_agent_response = ""
    for item in msg.content:
        if isinstance(item, TextContent):
            target_agent_response += item.text
    
    ctx.logger.info(f"Received response from {sender}: {target_agent_response[:100]}...")  # Truncate for logging

    #SET AGENT COMMAND
    if re.match(r"/agent[0-9A-Za-z]{39}/", target_agent_response):
        global TEST_TARGET_AGENT_ADDRESS
        TEST_TARGET_AGENT_ADDRESS = re.match(r"/agent[0-9A-Za-z]{39}/", target_agent_response).group(0)
        ctx.logger.info(f"Setting TEST_TARGET_AGENT_ADDRESS to {TEST_TARGET_AGENT_ADDRESS}")
        init_eval(ctx)
        return
    #PERFORM EVALUATION
    else:        
        eval_state.add_reponse(target_agent_response)
        eval_result = run_evaluator_agent(eval_state.currentEvalData, target_agent_response)

        if not eval_result:
            ctx.logger.error(f"No eval result found for question: {eval_state.currentQuestionId}")
            return

        eval_state.add_eval_result(
            eval_result["correctness"],
            eval_result["capabilities"],
            eval_result["domainKnowledge"],
            eval_result["speed"]
        )

        # eval_state.add_eval_result(
        #     1,0,0,0    
        # )
        
        ctx.logger.info(f"Total evaluations completed: 1")

########## HUMAN TO AGENT HANDLERS ##########
@eval_comms_agent.on_message(model=AIRequest, replies={AIResponse})
async def do_evaluation(ctx: Context, sender: str, msg: AIRequest):
    ctx.logger.info(f"Received question from {sender}: {msg.question}")

    message = AIResponse(text="Thanks for your response")
    await ctx.send(
        destination=sender, 
        message=message
    )

if __name__ == "__main__":
    eval_comms_agent.run()