from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv
from uagents import Agent, Context, Model
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    TextContent,
)
from openai import OpenAI
from langsmith import Client
from openevals.llm import create_llm_as_judge
from openevals.prompts import (
    CORRECTNESS_PROMPT,
    CONCISENESS_PROMPT, 
    HALLUCINATION_PROMPT,
    RAG_HELPFULNESS_PROMPT
)
from datetime import datetime, timezone
from uuid import uuid4
import random
import uuid
import re

# Load environment variables
# Default to local development - load from .env file
# Only skip dotenv when running on Railway
if not os.getenv("RAILWAY_ENVIRONMENT_ID"):
    # Running locally - load from .env file
    env_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path=env_path)
else:
    # Running on Railway - environment variables are already loaded
    pass

SEED_PHRASE = os.getenv("TRUTH_SWARM_AGENT_SEED_PHRASE")
if not SEED_PHRASE:
    raise ValueError("TRUTH_SWARM_AGENT_SEED_PHRASE environment variable not set")
if not os.getenv("LANGSMITH_API_KEY"):
    raise ValueError("LANGSMITH_API_KEY environment variable not set")
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable not set")
if not os.getenv("ASI1_API_KEY"):
    raise ValueError("ASI1_API_KEY environment variable not set")
if not os.getenv("LANGSMITH_TRACING"):
    raise ValueError("LANGSMITH_TRACING environment variable not set")
if not os.getenv("LANGSMITH_ENDPOINT"):
    raise ValueError("LANGSMITH_ENDPOINT environment variable not set")

# Instantiate agent agent1qtak6m7rgytst3zqmu744t0k8z4xytf3zrnct49efqvwxzqc3f3t5rkflj4
eval_comms_agent = Agent(
    name="truthswarm",
    seed=SEED_PHRASE,
    port=8000,
    mailbox=True,
    readme_path="README.md"
)

TEST_TARGET_AGENT_ADDRESS = "agent1q2c8sxs5kg902j96ffruh0he2erhjf63eahrypzvj20gjraevxlggy4fq33"

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
            "inputs": {"question": "What are the top 3 most popular travel destinations in Argentina in 2025?"},
            "outputs": {"answer": "Buenos Aires, Iguaza Falls, Patagonia"}
        }]},
    {"category": "defi", "evalData":
    [
        {
            "inputs": {"question": "What are the top 3 best performing crypto tokens in 2025?"},
            "outputs": {"answer": "Solana, XRP, Bitcoin"}
        },
    ]},
    {"category": "halloween", "evalData":
    [
        {
            "inputs": {"question": "Give me a creature that is a cross between a bull and a bee"},
            "outputs": {"answer": "Bull Bee"}
        },
    ]},
]

# STATE MANAGEMENT CLASS
class EvalState:
    def __init__(self):
        self.data_set_name = ""
        self.currentCategory = ""
        self.currentEvalData = None
        self.currentResponse = ""
        self.evalResults = {}
        self.agent = None
    
    def set_current_question(self, question_id, category):
        self.currentCategory = category

        # Set current data set name by generating a uuid
    def set_data_set_name(self):
        self.data_set_name = 'truth-swarm-' + str(uuid.uuid4())

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

################# CLASSES #################

@dataclass
class EvaluationScore:
    """Structure for agent evaluation score data that will be attested"""
    evaluatedAgentAddress: str
    evaluatorAgentAddress: str
    timestamp: int
    finalScore: int
    overallConfidence: int
    grade: str
    correctnessScore: int
    correctnessConfidence: int
    correctnessEffectiveScore: int
    correctnessWeight: int
    capabilitiesScore: int
    capabilitiesConfidence: int
    capabilitiesEffectiveScore: int
    capabilitiesWeight: int
    domainScore: int
    domainConfidence: int
    domainEffectiveScore: int
    domainWeight: int
    detailsCID: str


################# EVAL UTIL FUNCTIONS #################
def run_evaluation_correctness_task(inputs: dict, outputs: dict, reference_outputs: dict):
    #print the inputs, outputs and reference outputs
    print("Running evaluation correctness task...")
    print("Inputs: ", inputs)
    print("Outputs: ", outputs)
    print("Reference Outputs: ", reference_outputs)
    evaluator = create_llm_as_judge(
        prompt=CORRECTNESS_PROMPT,
        model="openai:o3-mini",
        feedback_key="correctness",
    )
    eval_result = evaluator(
        inputs=inputs,
        outputs=outputs,
        reference_outputs=reference_outputs
    )
    return eval_result    

def target(tested_agent_response) -> dict:
    return { "answer": tested_agent_response.strip() }

def create_dataset(eval_data):
    print("Creating new dataset: evaluator_dataset")
    # https://smith.langchain.com/onboarding?organizationId=44cc621b-830d-4ea0-b5d5-be6b304c547e&step=4
    
    # Create dataset and register name with state
    eval_state.set_data_set_name()
    dataset = langsmith_client.create_dataset(
        dataset_name=eval_state.data_set_name,
        description="Dataset for evaluator agent"     
    )
    
    # Add examples only when creating new dataset
    langsmith_client.create_examples(
        dataset_id=dataset.id,
        examples=eval_data
    )
    
    return dataset

def create_evaluators():
    return [
        create_llm_as_judge(
            prompt=CORRECTNESS_PROMPT,
            model="openai:o3-mini",
            feedback_key="correctness",
            continuous=True
        ),
        create_llm_as_judge(
            prompt=CONCISENESS_PROMPT,
            model="openai:o3-mini", 
            feedback_key="conciseness",
            continuous=True
        ),
        # create_llm_as_judge(
        #     prompt=HALLUCINATION_PROMPT,
        #     model="openai:o3-mini",
        #     feedback_key="hallucination",
        #     continuous=True
        # ),
        create_llm_as_judge(
            prompt=RAG_HELPFULNESS_PROMPT,
            model="openai:o3-mini",
            feedback_key="helpfulness",
            continuous=True
        )
    ]

################# EVALUATOR AGENT #################
subject_matter = "Return ONLY valid JSON matching the provided schema. You are an evaluator agent that evaluates the performance of other agents in a game. You evaluate the agent's responses and provide a rating for each category by evaluating the input json expected key."

langsmith_client = Client()

def run_evaluator_agent(eval_data, tested_agent_response):
    response = 'I am afraid something went wrong and I am unable to answer your question at the moment'
    
    if not eval_data or not tested_agent_response:
        print("No eval data or tested agent response")
        return response

    # Reuse existing dataset or create it once
    if eval_state.data_set_name:
        # Dataset name exists, try to read it
        try:
            dataset = langsmith_client.read_dataset(dataset_name=eval_state.data_set_name)
            print("Reusing existing dataset: " + eval_state.data_set_name)
        except:
            dataset = create_dataset(eval_data)
    else:
        dataset = create_dataset(eval_data)
    
    print("Running test scoring...")
    print(f"Eval data: {eval_data}")
    print(f"Agent response: {tested_agent_response}")
    
    # Create a proper target function for this specific response
    def evaluation_target(inputs):
        # Return the actual agent response we want to evaluate
        # Provide context for evaluators that need it (hallucination, helpfulness)
        return {
            "answer": tested_agent_response,
            "context": inputs.get("question", "")
        }

    evaluators = create_evaluators()

    # Run LangSmith evaluation
    try:
        # Use the dataset object for evaluation
        langsmith_response = langsmith_client.evaluate(
            evaluation_target,
            data=dataset,  # Pass the dataset object
            evaluators=evaluators,
            experiment_prefix="truth-swarm",
            max_concurrency=2
        )
        
        # Wait for evaluation to complete before accessing results
        langsmith_response.wait()
        
        # Access the _results attribute which contains the evaluation data
        results = langsmith_response._results[0]["evaluation_results"]["results"]
        if not results:
            return None
        print(f"Found {len(results)} evaluation results")
        return results
        
    except Exception as e:
        print(f"LangSmith evaluation failed: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        raise e  # Re-raise to see the full error


################# SCORING #################
def generate_score(tested_agent_address: str, ctx: Context, eval_result) -> EvaluationScore:
        """Generate realistic mock evaluation scores for demo/hackathon"""
        
        # Extract correctness score from evaluation results
        correctness_score = None
        conciseness_score = None
        hallucination_score = None
        helpfulness_score = None

        if eval_result and isinstance(eval_result, list) and len(eval_result) > 0:
            # Look for feedback in the results - EvaluationResult has key and score attributes
            for result in eval_result:
                try:
                    # Access score directly from the result object
                    if hasattr(result, 'key') and hasattr(result, 'score'):
                        score_value = int(result.score * 100) if result.score is not None else None
                        
                        if result.key == 'correctness' and score_value is not None:
                            correctness_score = score_value
                            ctx.logger.info(f"✓ Correctness score: {correctness_score}")
                        elif result.key == 'conciseness' and score_value is not None:
                            conciseness_score = score_value
                            ctx.logger.info(f"✓ Conciseness score: {conciseness_score}")
                        elif result.key == 'hallucination' and score_value is not None:
                            hallucination_score = score_value
                            ctx.logger.info(f"✓ Hallucination score: {hallucination_score}")
                        elif result.key == 'helpfulness' and score_value is not None:
                            helpfulness_score = score_value
                            ctx.logger.info(f"✓ Helpfulness score: {helpfulness_score}")
                except Exception as e:
                    ctx.logger.warning(f"Failed to extract score from result: {e}")
                    continue

        capabilities_score = random.randint(70, 90)
        domain_score = random.randint(80, 95)
        
        # Weights (should sum to 100)
        correctness_weight = 40
        capabilities_weight = 30
        domain_weight = 30
        
        # Calculate effective scores (weighted)
        correctness_effective = (correctness_score * correctness_weight) // 100
        capabilities_effective = (capabilities_score * capabilities_weight) // 100
        domain_effective = (domain_score * domain_weight) // 100
        
        final_score = correctness_effective + capabilities_effective + domain_effective
        
        # Assign grade
        if final_score >= 90:
            grade = "A+"
        elif final_score >= 85:
            grade = "A"
        elif final_score >= 80:
            grade = "B+"
        elif final_score >= 75:
            grade = "B"
        else:
            grade = "C+"
        
        ctx.logger.info(f"📊 Generated evaluation: Score={final_score}/100, Grade={grade}")
        
        return EvaluationScore(
            evaluatedAgentAddress=tested_agent_address,
            evaluatorAgentAddress=str(eval_comms_agent.address),
            timestamp=int(datetime.now(timezone.utc).timestamp()),
            finalScore=final_score,
            overallConfidence=8,
            grade=grade,
            correctnessScore=correctness_score,
            correctnessConfidence=8,
            correctnessEffectiveScore=correctness_effective,
            correctnessWeight=correctness_weight,
            capabilitiesScore=capabilities_score,
            capabilitiesConfidence=7,
            capabilitiesEffectiveScore=capabilities_effective,
            capabilitiesWeight=capabilities_weight,
            domainScore=domain_score,
            domainConfidence=9,
            domainEffectiveScore=domain_effective,
            domainWeight=domain_weight,
            detailsCID=f"bafkreimock{random.randint(1000, 9999)}evaluation"
        )

################# UTILITY FUNCTIONS #################

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
    
    # Send to target agent using ChatMessage format
    await ctx.send(
        destination=TEST_TARGET_AGENT_ADDRESS, 
        message=ChatMessage(
            timestamp=datetime.now(),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=evalData[0]["inputs"]["question"])]
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
        
        #TODO: send eval result to badging agent
        print(f"LangSmith evaluation completed!")

        generate_score(TEST_TARGET_AGENT_ADDRESS, ctx, eval_result)

        ctx.logger.info(f"Evaluation completed for {sender}")
        ctx.logger.info(f"Evaluation result: {eval_result}")
        
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