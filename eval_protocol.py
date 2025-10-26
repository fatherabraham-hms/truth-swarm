"""
Evaluation Protocol for Evaluator Agent

Handles direct agent-to-agent evaluation requests via uAgents protocol.
"""

from uagents import Agent, Context, Protocol, Model
from typing import Optional


class EvaluationRequest(Model):
    """Request to evaluate an agent"""
    agent_address: str
    evaluation_type: str = "comprehensive"
    requester: str = ""


class EvaluationResponse(Model):
    """Response with evaluation and attestation"""
    success: bool
    agent_address: str
    attestation_uid: Optional[str] = None
    final_score: int
    grade: str
    message: str
    error: Optional[str] = None


def create_evaluation_protocol(agent: Agent, process_evaluation_func) -> Protocol:
    """
    Create and configure the evaluation protocol
    
    Args:
        agent: The uAgent instance
        process_evaluation_func: Function to call for evaluations
        
    Returns:
        Configured evaluation protocol
    """
    eval_proto = Protocol(name="evaluation_protocol", version="1.0")

    @eval_proto.on_message(model=EvaluationRequest, replies=EvaluationResponse)
    async def handle_eval_request(ctx: Context, sender: str, msg: EvaluationRequest):
        """Handle direct protocol-based evaluation requests from other agents"""
        ctx.logger.info(f"📨 Protocol evaluation request from {sender} for: {msg.agent_address}")
        
        result = await process_evaluation_func(msg.agent_address, ctx)
        await ctx.send(sender, result)

    return eval_proto

