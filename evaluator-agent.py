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

# Blockchain/EAS interaction
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from eth_abi import encode
from typing import Optional

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
if not os.getenv("RPC_URL"):
    raise ValueError("RPC_URL environment variable not set")
if not os.getenv("EAS_CONTRACT_ADDRESS"):
    raise ValueError("EAS_CONTRACT_ADDRESS environment variable not set")
if not os.getenv("PRIVATE_KEY"):
    raise ValueError("PRIVATE_KEY environment variable not set")
if not os.getenv("CHAIN_ID"):
    raise ValueError("CHAIN_ID environment variable not set")

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
        self.requesterAddress = ""
        self.currentCategory = ""
        self.currentEvalData = None
        self.currentResponse = ""
        self.evalResults = {}
        self.agent = None
    def set_requester_address(self, requester_address):
        self.requesterAddress = requester_address
    def get_requester_address(self):
        return self.requesterAddress
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


################# ATTESTATION MANAGER #################
class AttestationManager:
    """Manages EAS attestations for agent evaluations"""
    
    AGENT_EVALUATION_SCHEMA_UID = "0xcd0ab40423e8919b72b665cb563c82b895acc2b690626f2c8180e1db83f6f5bc"
    
    def __init__(self):
        # Load configuration from environment
        self.rpc_url = os.getenv('RPC_URL', 'https://sepolia.infura.io/v3/YOUR_PROJECT_ID')
        self.eas_contract_address = os.getenv('EAS_CONTRACT_ADDRESS', '0xC2679fBD37d54388Ce493F1DB75320D236e1815e')
        self.resolver_contract_address = os.getenv('RESOLVER_CONTRACT_ADDRESS', '')
        self.private_key = os.getenv('PRIVATE_KEY')
        self.chain_id = int(os.getenv('CHAIN_ID', '11155111'))  # Sepolia
        self.enabled = bool(self.private_key)
        
        if not self.enabled:
            print("⚠️  PRIVATE_KEY not set - attestation disabled (using mock mode)")
            return
        
        try:
            # Initialize Web3
            self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
            self.w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
            
            # Set up account
            self.account = self.w3.eth.account.from_key(self.private_key)
            self.address = self.account.address
            
            # Initialize EAS contract
            self.eas_contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(self.eas_contract_address),
                abi=self._get_eas_abi()
            )
            
            print(f"✅ Attestation manager initialized with address: {self.address}")
        except Exception as e:
            print(f"⚠️  Attestation manager initialization failed: {e}")
            self.enabled = False
    
    def _get_eas_abi(self):
        """
        Minimal EAS ABI for attestation
        
        Matches the deployed EAS contract on Sepolia (0xC2679fBD37d54388Ce493F1DB75320D236e1815e)
        Updated to match actual contract ABI for proper event parsing
        """
        return [
            {
                "inputs": [
                    {
                        "components": [
                            {"internalType": "bytes32", "name": "schema", "type": "bytes32"},
                            {
                                "components": [
                                    {"internalType": "address", "name": "recipient", "type": "address"},
                                    {"internalType": "uint64", "name": "expirationTime", "type": "uint64"},
                                    {"internalType": "bool", "name": "revocable", "type": "bool"},
                                    {"internalType": "bytes32", "name": "refUID", "type": "bytes32"},
                                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                                    {"internalType": "uint256", "name": "value", "type": "uint256"}
                                ],
                                "internalType": "struct AttestationRequestData",
                                "name": "data",
                                "type": "tuple"
                            }
                        ],
                        "internalType": "struct AttestationRequest",
                        "name": "request",
                        "type": "tuple"
                    }
                ],
                "name": "attest",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "payable",
                "type": "function"
            },
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "internalType": "address", "name": "recipient", "type": "address"},
                    {"indexed": True, "internalType": "address", "name": "attester", "type": "address"},
                    {"indexed": False, "internalType": "bytes32", "name": "uid", "type": "bytes32"},
                    {"indexed": True, "internalType": "bytes32", "name": "schema", "type": "bytes32"}
                ],
                "name": "Attested",
                "type": "event"
            }
        ]
    
    def _encode_evaluation_data(self, evaluation: EvaluationScore) -> bytes:
        """Encode evaluation score data for EAS schema"""
        types = [
            'string', 'string', 'uint256', 'uint256', 'uint8', 'string',
            'uint256', 'uint8', 'uint256', 'uint8', 'uint256', 'uint8',
            'uint256', 'uint8', 'uint256', 'uint8', 'uint256', 'uint8', 'string'
        ]
        
        values = [
            evaluation.evaluatedAgentAddress,
            evaluation.evaluatorAgentAddress,
            evaluation.timestamp,
            evaluation.finalScore,
            evaluation.overallConfidence,
            evaluation.grade,
            evaluation.correctnessScore,
            evaluation.correctnessConfidence,
            evaluation.correctnessEffectiveScore,
            evaluation.correctnessWeight,
            evaluation.capabilitiesScore,
            evaluation.capabilitiesConfidence,
            evaluation.capabilitiesEffectiveScore,
            evaluation.capabilitiesWeight,
            evaluation.domainScore,
            evaluation.domainConfidence,
            evaluation.domainEffectiveScore,
            evaluation.domainWeight,
            evaluation.detailsCID
        ]
        
        return encode(types, values)
    
    async def create_attestation(self, evaluation: EvaluationScore) -> Optional[str]:
        """Create attestation on EAS"""
        if not self.enabled:
            # Return mock UID for demo
            mock_uid = f"0x{''.join(random.choices('0123456789abcdef', k=64))}"
            print(f"🔧 Mock attestation UID generated: {mock_uid}")
            return mock_uid
        
        try:
            # Prepare attestation data
            attestation_data = self._encode_evaluation_data(evaluation)
            
            # Build transaction
            nonce = self.w3.eth.get_transaction_count(self.address)
            
            # Create nested tuple structure matching EAS ABI:
            # attest(tuple(bytes32 schema, tuple(address recipient, uint64 expirationTime,
            #        bool revocable, bytes32 refUID, bytes data, uint256 value) data) request)
            
            # Match TypeScript structure from agent-attestation.ts lines 54-64
            # Inner tuple: (recipient, expirationTime, revocable, refUID, data, value)
            inner_data_tuple = (
                Web3.to_checksum_address("0x0000000000000000000000000000000000000000"),  # recipient
                0,  # expirationTime (no expiration)
                False,  # revocable
                b'\x00' * 32,  # refUID (no reference)
                attestation_data,  # encoded evaluation data
                0  # value (no ETH sent)
            )
            
            # Outer tuple: (schema, data) - this is the SINGLE "request" parameter
            attestation_request_tuple = (
                Web3.to_bytes(hexstr=self.AGENT_EVALUATION_SCHEMA_UID),  # schema
                inner_data_tuple  # nested data tuple
            )
            
            # Pass the tuple directly - web3.py will treat this as a single parameter
            transaction = self.eas_contract.functions.attest(
                attestation_request_tuple
            ).build_transaction({
                'from': self.address,
                'gas': 1000000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
                'chainId': self.chain_id
            })
            
            # Sign and send
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            print(f"📤 Attestation transaction sent: {tx_hash.hex()}")
            
            # Wait for receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt.status == 1:
                # Extract UID from event logs
                logs = self.eas_contract.events.Attested().process_receipt(receipt)
                if logs:
                    attestation_uid = logs[0]['args']['uid'].hex()
                    print(f"✅ Attestation created: {attestation_uid}")
                    return attestation_uid
                else:
                    # Fallback to tx hash if event parsing fails
                    return f"0x{tx_hash.hex()}"
            
            return None
            
        except Exception as e:
            print(f"❌ Error creating attestation: {e}")
            return None


################# EVAL UTIL FUNCTIONS #################
def run_evaluations(inputs: dict, outputs: dict, reference_outputs: dict):
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
attestation_manager = AttestationManager()

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
        if final_score >= 95:
            grade = "A+"
        elif final_score >= 90:
            grade = "A"
        elif final_score >= 85:
            grade = "B+"
        elif final_score >= 80:
            grade = "B"
        elif final_score >= 75:
            grade = "C+"
        elif final_score >= 70:
            grade = "C"
        elif final_score >= 65:
            grade = "D+"
        else:
            grade = "D"
        
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

async def sendConfirmationToRequester(ctx: Context, requester_address: str, target_agent_address: str, message: str):
    await ctx.send(
        destination=requester_address, 
        message=AIResponse(text=message)
    )

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
        # record the requester address
        eval_state.set_requester_address(sender)
        await sendConfirmationToRequester(ctx, sender, TEST_TARGET_AGENT_ADDRESS, f"Evaluation started for {TEST_TARGET_AGENT_ADDRESS}")
        init_eval(ctx)
        return
    #PERFORM EVALUATION BASED ON TARGET AGENT RESPONSE
    else:        
        eval_state.add_reponse(target_agent_response)
        await sendConfirmationToRequester(ctx, sender, TEST_TARGET_AGENT_ADDRESS, f"Received response from {TEST_TARGET_AGENT_ADDRESS}.")
        eval_result = run_evaluator_agent(eval_state.currentEvalData, target_agent_response)
        
        ctx.logger.info(f"LangSmith evaluation completed!")
        await sendConfirmationToRequester(ctx, sender, TEST_TARGET_AGENT_ADDRESS, f"Evaluation completed successfully for {TEST_TARGET_AGENT_ADDRESS}")
        # Generate evaluation score
        evaluation_score = generate_score(TEST_TARGET_AGENT_ADDRESS, ctx, eval_result)
        
        # Create attestation on EAS blockchain
        ctx.logger.info("🔗 Creating attestation on EAS...")
        attestation_uid = await attestation_manager.create_attestation(evaluation_score)
        
        if attestation_uid:
            ctx.logger.info(f"✅ Attestation created: {attestation_uid}")
            ctx.logger.info(f"📊 Score: {evaluation_score.finalScore}/100 ({evaluation_score.grade})")
        else:
            ctx.logger.warning("⚠️  Failed to create attestation on EAS")
        await sendConfirmationToRequester(ctx, sender, TEST_TARGET_AGENT_ADDRESS, f"Attestation created: {attestation_uid}")
        ctx.logger.info(f"Evaluation completed for {sender}")
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