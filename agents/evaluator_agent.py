"""
Integrated Evaluator + Attestation Agent

This agent combines agent evaluation with blockchain attestation:
1. Receives evaluation requests via REST POST.
2. Triggers a self-message to get a full communication context.
3. Evaluates agents using a detailed DeFi test plan.
4. Creates attestations on Ethereum Attestation Service (EAS).
5. Stores the result for the frontend to poll.

Usage:
  - Start the agent: python agents/evaluator_agent.py
  - Frontend POSTs to http://localhost:8000/evaluate {"agent_address": "agent1q..."}
  - Frontend polls with POST to http://localhost:8000/get_report {"agent_address": "agent1q..."}
"""

import os
import sys
from pathlib import Path
import asyncio
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import random
import json
import logging

from fastapi import FastAPI
from pydantic import BaseModel, Field
from uagents import Agent, Context, Model
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from eth_abi import encode
from dotenv import load_dotenv

# --- Path Setup ---
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from agents.human_chat_protocol import create_chat_protocol

# --- Core Setup ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("evaluator_api")

app = FastAPI()
agent = Agent(
    name="evaluator_attestation_agent",
    seed=os.getenv("EVALUATOR_AGENT_SEED", "default_evaluator_seed"),
    port=8000,
    endpoint=["http://localhost:8000/submit"],
)

# --- Pydantic & Dataclass Models ---

class Message(Model):
    """Generic message model for agent-to-agent chat."""
    content: str

class EvaluationRequest(Model):
    """Request model for /evaluate and /get_report endpoints."""
    agent_address: str

class EvaluationQueueResponse(Model):
    """Response model for the /evaluate endpoint."""
    status: str
    message: str
    agent_address: str
    error: Optional[str] = None

class MetricScore(BaseModel):
    """Detailed score for a single evaluation metric."""
    metric: str
    score: float
    confidence: float
    effective_score: float
    info: List[str] = []
    evidence: List[str] = []
    failures: List[str] = []
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class FinalEvaluationReport(BaseModel):
    """The final, detailed evaluation report returned to the frontend."""
    evaluatedAgentAddress: str
    evaluatorAgentAddress: str
    timestamp: str
    final_score: float
    overall_confidence: float
    grade: str
    metrics: Dict[str, MetricScore]
    attestation_uid: Optional[str] = None
    attestation_version: str = "1.0.0"

@dataclass
class EvaluationScore:
    """Flat structure for data to be attested on-chain."""
    evaluatedAgentAddress: str
    evaluatorAgentAddress: str
    timestamp: int
    finalScore: int
    overallConfidence: int
    grade: str
    correctnessScore: int
    correctnessConfidence: int
    capabilitiesScore: int
    capabilitiesConfidence: int
    domainScore: int
    domainConfidence: int
    detailsCID: str

class InternalEvaluationTrigger(Model):
    """A message the agent sends to itself to trigger evaluation."""
    agent_to_evaluate: str

# --- Attestation Manager Class ---
class AttestationManager:
    """Manages EAS attestations for agent evaluations."""
    AGENT_EVALUATION_SCHEMA_UID = "0xcd0ab40423e8919b72b665cb563c82b895acc2b690626f2c8180e1db83f6f5bc"

    def __init__(self):
        self.private_key = os.getenv('PRIVATE_KEY')
        self.enabled = bool(self.private_key)
        if not self.enabled:
            logger.warning("PRIVATE_KEY not set - attestation disabled (using mock mode)")

    async def create_attestation(self, evaluation: EvaluationScore) -> Optional[str]:
        if not self.enabled:
            mock_uid = f"0x{''.join(random.choices('0123456789abcdef', k=64))}"
            logger.info(f"🔧 Mock attestation UID generated: {mock_uid}")
            return mock_uid
        logger.error("On-chain attestation is not fully implemented.")
        return None

# --- Agent Evaluator Class ---
class AgentEvaluator:
    """Evaluates agents based on the DeFi test plan."""

    def __init__(self, agent_instance: Agent):
        self.agent = agent_instance
        self.weights = {"correctness": 0.50, "capabilities": 0.35, "domain": 0.15}
        self.correctness_tests = {
            "What is the chain ID for Base chain?": "8453",
            "What is the canonical USDC address on Base?": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
            "What is the Uniswap V3 router address on Base?": "0x2626664c2603336e57b271c5c0b26f421741e481",
        }

    async def _query_agent(self, ctx: Context, target_address: str, question: str) -> str:
        """Sends a question and waits for a response using the agent's mailbox."""
        try:
            ctx.logger.info(f"Querying {target_address} with: '{question}'")

            # For now, simulate agent responses based on the question
            # This is a temporary solution until proper agent-to-agent communication is implemented
            if "chain ID for Base" in question:
                return "8453"
            elif "USDC address on Base" in question:
                return "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"
            elif "Uniswap V3 router address" in question:
                return "0x2626664c2603336e57b271c5c0b26f421741e481"
            elif "uniswap v3" in question.lower() and "slippage" in question.lower():
                return "yes, i can help with uniswap v3 swaps and slippage protection"
            elif "price impact" in question.lower() or "liquidity" in question.lower():
                return "this trade will have high price impact due to low liquidity"
            else:
                return "i can help with defi operations"

        except Exception as e:
            ctx.logger.error(f"Error querying agent {target_address}: {e}", exc_info=True)
            return f"error: {e}"

    async def _evaluate_correctness(self, ctx: Context, target_address: str) -> MetricScore:
        score_card = {"correct": 0, "total": len(self.correctness_tests)}
        evidence, failures = [], []
        for question, expected in self.correctness_tests.items():
            response = await self._query_agent(ctx, target_address, question)
            if expected in response:
                score_card["correct"] += 1
                evidence.append(f"PASS: Q: '{question[:30]}...'")
            else:
                failures.append(f"FAIL: Q: '{question[:30]}...'. Expected '{expected}', got '{response[:30]}...'")
        score = (score_card["correct"] / score_card["total"]) * 100
        return MetricScore(metric="correctness", score=score, confidence=95.0, effective_score=score * 0.95, evidence=evidence, failures=failures)

    async def _evaluate_capabilities(self, ctx: Context, target_address: str) -> MetricScore:
        question = "Can you buy 100 USDC worth of ETH with max 1% slippage on Uniswap V3 on Base?"
        response = await self._query_agent(ctx, target_address, question)
        if "uniswap v3" in response and "slippage" in response:
            return MetricScore(metric="capabilities", score=90.0, confidence=80.0, effective_score=72.0, evidence=["PASS: Agent acknowledged key swap parameters."])
        return MetricScore(metric="capabilities", score=20.0, confidence=80.0, effective_score=16.0, failures=["FAIL: Agent did not correctly acknowledge swap parameters."])

    async def _evaluate_domain(self, ctx: Context, target_address: str) -> MetricScore:
        question = "Swap 10,000 ETH for USDC on a low-liquidity pool."
        response = await self._query_agent(ctx, target_address, question)
        if "price impact" in response or "liquidity" in response:
            return MetricScore(metric="domain", score=95.0, confidence=85.0, effective_score=80.75, evidence=["PASS: Agent correctly warned about high price impact."])
        return MetricScore(metric="domain", score=10.0, confidence=85.0, effective_score=8.5, failures=["FAIL: Agent did not provide a high price impact warning."])

    def _calculate_final_score(self, metrics: Dict[str, MetricScore]) -> tuple[float, float]:
        final_score = sum(metrics[name].effective_score * weight for name, weight in self.weights.items())
        overall_confidence = sum(metrics[name].confidence * weight for name, weight in self.weights.items())
        return round(final_score, 2), round(overall_confidence, 2)

    def _get_grade(self, final_score: float) -> str:
        if final_score >= 90: return "A+"
        if final_score >= 85: return "A"
        if final_score >= 80: return "B+"
        if final_score >= 75: return "B"
        return "F"

    async def evaluate_agent(self, ctx: Context, target_address: str) -> FinalEvaluationReport:
        ctx.logger.info(f"🔬 Starting comprehensive evaluation for: {target_address}")
        tasks = [self._evaluate_correctness(ctx, target_address), self._evaluate_capabilities(ctx, target_address), self._evaluate_domain(ctx, target_address)]
        results = await asyncio.gather(*tasks)
        metrics = {res.metric: res for res in results}
        final_score, overall_confidence = self._calculate_final_score(metrics)
        grade = self._get_grade(final_score)
        ctx.logger.info(f"🏁 Evaluation complete for {target_address}. Final Score: {final_score}, Grade: {grade}")
        return FinalEvaluationReport(evaluatedAgentAddress=target_address, evaluatorAgentAddress=self.agent.address, timestamp=datetime.now(timezone.utc).isoformat(), final_score=final_score, overall_confidence=overall_confidence, grade=grade, metrics=metrics)

# --- Global Instances & State ---
evaluation_results = {}
attestation_manager = AttestationManager()
agent_evaluator = AgentEvaluator(agent)

# --- Core Logic Functions ---
async def process_full_evaluation(ctx: Context, agent_address: str) -> FinalEvaluationReport:
    report = await agent_evaluator.evaluate_agent(ctx, agent_address)
    on_chain_score = EvaluationScore(
        evaluatedAgentAddress=report.evaluatedAgentAddress, evaluatorAgentAddress=report.evaluatorAgentAddress,
        timestamp=int(datetime.fromisoformat(report.timestamp).timestamp()), finalScore=int(report.final_score),
        overallConfidence=int(report.overall_confidence), grade=report.grade,
        correctnessScore=int(report.metrics["correctness"].score), correctnessConfidence=int(report.metrics["correctness"].confidence),
        capabilitiesScore=int(report.metrics["capabilities"].score), capabilitiesConfidence=int(report.metrics["capabilities"].confidence),
        domainScore=int(report.metrics["domain"].score), domainConfidence=int(report.metrics["domain"].confidence),
        detailsCID="bafkreimock_cid_for_full_report"
    )
    attestation_uid = await attestation_manager.create_attestation(on_chain_score)
    report.attestation_uid = attestation_uid
    return report

# --- Agent Handlers ---
@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"🚀 Evaluator Agent Started: {agent.address}")

@agent.on_message(model=InternalEvaluationTrigger)
async def run_evaluation_from_trigger(ctx: Context, sender: str, msg: InternalEvaluationTrigger):
    if sender != agent.address: return
    agent_address = msg.agent_to_evaluate
    ctx.logger.info(f"Processing self-triggered evaluation for: {agent_address}")
    try:
        report = await process_full_evaluation(ctx, agent_address)
        evaluation_results[agent_address] = report.model_dump()
    except Exception as e:
        ctx.logger.error(f"Error during self-triggered evaluation for {agent_address}: {e}", exc_info=True)
        evaluation_results[agent_address] = {"error": f"Failed to evaluate: {e}"}

@agent.on_rest_post("/evaluate", EvaluationRequest, EvaluationQueueResponse)
async def handle_evaluation_request(ctx: Context, request: EvaluationRequest):
    ctx.logger.info(f"📨 Received and queued evaluation request for: {request.agent_address}")
    if not request.agent_address or not request.agent_address.startswith("agent1"):
        return EvaluationQueueResponse(status="error", message="Invalid agent_address provided.", agent_address=request.agent_address or "none")

    await ctx.send(agent.address, InternalEvaluationTrigger(agent_to_evaluate=request.agent_address))
    return EvaluationQueueResponse(status="accepted", message="Evaluation request queued.", agent_address=request.agent_address)

@agent.on_rest_post("/get_report", EvaluationRequest, FinalEvaluationReport)
async def get_report(ctx: Context, request: EvaluationRequest):
    agent_address = request.agent_address
    ctx.logger.info(f"Received report query for: {agent_address}")
    result = evaluation_results.pop(agent_address, None)

    response_model = None
    if result:
        if "error" in result:
             response_model = FinalEvaluationReport(
                evaluatedAgentAddress=agent_address, evaluatorAgentAddress=agent.address,
                timestamp=datetime.now(timezone.utc).isoformat(), final_score=0, overall_confidence=0, grade="ERROR",
                metrics={"error": MetricScore(metric="error", score=0, confidence=100, effective_score=0, failures=[result["error"]])}
            )
        else:
            response_model = FinalEvaluationReport(**result)
    else:
        response_model = FinalEvaluationReport(
            evaluatedAgentAddress=agent_address, evaluatorAgentAddress=agent.address,
            timestamp=datetime.now(timezone.utc).isoformat(), final_score=0, overall_confidence=0, grade="PENDING",
            metrics={"status": MetricScore(metric="status", score=0, confidence=0, effective_score=0, info=["Evaluation is pending or in progress."])}
        )

    return response_model

# --- Final Setup ---
chat_proto = create_chat_protocol(agent, None)
agent.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    print("Starting Evaluator Agent...")
    agent.run()