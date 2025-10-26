"""
Chat Protocol for Evaluator Agent

Handles conversational interaction focused on agent evaluation.

Features:
- ASI:1 Mini LLM for general knowledge questions
- Direct agent address detection and evaluation
- Keyword-based evaluation request detection
- Seamless switching between chat and evaluation modes
"""

import os
import re
from datetime import datetime, timezone
from uuid import uuid4

import aiohttp

from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)


class ASI1ChatHandler:
    """
    Chat handler with ASI:1 Mini LLM for general knowledge
    Switches to evaluation mode when agent addresses are detected
    """
    
    def __init__(self, agent: Agent, process_evaluation_func):
        self.agent = agent
        self.process_evaluation = process_evaluation_func
        # ASI:1 Mini model endpoint
        self.asi1_url = "https://api.asi1.ai/v1/chat/completions"
        self.api_key = os.getenv('ASI_ONE_API_KEY', '')
        
        # Debug: Check if API key is loaded
        if self.api_key:
            print(f"✅ ASI_ONE_API_KEY loaded (length: {len(self.api_key)})")
        else:
            print("⚠️  ASI_ONE_API_KEY not found in environment variables!")
    
    async def chat(self, message: str, session_id: str, ctx: Context) -> str:
        """Process chat message - use ASI:1 for general knowledge or evaluate agents"""
        
        # Priority 1: Check for direct agent address (evaluation request)
        agent_match = re.search(r'agent1[a-z0-9]{59}', message)
        if agent_match:
            ctx.logger.info(f"🎯 Evaluation request detected: {agent_match.group(0)}")
            result = await self.process_evaluation(agent_match.group(0), ctx)
            return self._format_evaluation_result(result)
        
        # Priority 2: Use ASI:1 Mini for general knowledge
        ctx.logger.info(f"💭 Using ASI:1 Mini for general query")
        return await self._ask_asi1(message, session_id, ctx)
    
    async def _ask_asi1(self, message: str, session_id: str, ctx: Context) -> str:
        """Query ASI:1 Mini model for general knowledge"""
        try:
            system_prompt = """You are a helpful AI assistant for Truth Swarm, an agent evaluation platform.

You can answer general questions about anything. When users ask about agent evaluation:
- Explain that you can evaluate agents by providing their address (65 characters starting with 'agent1')
- Mention evaluations cover: Correctness (40%), Capabilities (30%), Domain Knowledge (30%)
- Note that evaluations are stored on-chain via Ethereum Attestation Service (EAS)

Keep responses concise, helpful, and friendly. If you don't know something, just say so."""

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.asi1_url,
                    json={
                        "model": "asi1-mini",  # Minimal ASI:1 model
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": message}
                        ]
                    },
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['choices'][0]['message']['content']
                    else:
                        error_text = await response.text()
                        ctx.logger.warning(f"ASI:1 API returned {response.status}: {error_text}")
                        return self._fallback_response(message)
        except Exception as e:
            ctx.logger.error(f"ASI:1 error: {e}")
            return self._fallback_response(message)
    
    def _format_evaluation_result(self, result) -> str:
        """Format evaluation result for chat display"""
        if result.success:
            # Use the detailed message from the evaluation result if available
            if hasattr(result, 'message') and result.message:
                return result.message
            else:
                # Fallback to basic format if no detailed message
                return f"""✅ Agent Evaluation Complete!

📊 Final Score: {result.final_score}/100
🎓 Grade: {result.grade}
🔗 Attestation UID: {result.attestation_uid}

🔍 View on EAS Explorer:
https://sepolia.easscan.org/attestation/view/{result.attestation_uid}

The evaluation has been permanently recorded on-chain via Ethereum Attestation Service.

Ask me anything else about this evaluation or evaluate another agent!"""
        else:
            return f"""❌ Evaluation Failed

Error: {result.error}

Please check the agent address and try again."""
    
    def _fallback_response(self, message: str) -> str:
        """Fallback when ASI:1 is not available"""
        lower_msg = message.lower()

        # Provide helpful responses based on keywords
        if any(word in lower_msg for word in ['how', 'what', 'explain', 'work']):
            return """💡 About Agent Evaluation

I evaluate AI agents across three dimensions:
• Correctness (40%): Accuracy and reliability
• Capabilities (30%): Features and functionality  
• Domain Knowledge (30%): Specialized expertise

Evaluations are stored on-chain as EAS attestations, creating a permanent trust record.

To evaluate an agent, send me an agent address (65 characters starting with 'agent1')."""

        if any(word in lower_msg for word in ['hello', 'hi', 'hey']):
            return """👋 Hello! I'm your Truth Swarm assistant.

I can answer general questions and evaluate AI agents.

To evaluate an agent, just send me their address (starts with 'agent1', 65 characters).

What would you like to know?"""

        return """👋 I'm here to help!

I can answer questions and evaluate AI agents. To evaluate an agent, send me their address (starts with 'agent1').

Example: agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y

What can I help you with?"""


def create_text_chat(text: str, end_session: bool = True) -> ChatMessage:
    """Create chat message with text content"""
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(timestamp=datetime.now(timezone.utc), msg_id=uuid4(), content=content)


def create_chat_protocol(agent: Agent, process_evaluation_func) -> Protocol:
    """
    Create and configure the chat protocol for agent evaluation
    
    Args:
        agent: The uAgent instance
        process_evaluation_func: Function to call for evaluations
        
    Returns:
        Configured chat protocol
    """
    # Initialize chat handler with ASI:1 Mini for general knowledge
    chat_handler = ASI1ChatHandler(agent, process_evaluation_func)
    
    # Create protocol
    chat_proto = Protocol(spec=chat_protocol_spec)

    @chat_proto.on_message(ChatMessage)
    async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
        """Handle chat messages"""

        # Send acknowledgement
        await ctx.send(sender, ChatAcknowledgement(
            timestamp=datetime.now(timezone.utc),
            acknowledged_msg_id=msg.msg_id
        ))

        # Welcome message on session start
        if any(isinstance(item, StartSessionContent) for item in msg.content):
            await ctx.send(sender, create_text_chat(
                chat_handler._fallback_response(""),
                end_session=False
            ))
            return

        # Get message text
        text = msg.text()
        if not text:
            return

        ctx.logger.info(f"📨 Chat message from {sender}: {text}")

        # Generate session ID from message
        session_id = str(msg.msg_id)

        # Process through chat handler
        response = await chat_handler.chat(text, session_id, ctx)

        # Send response
        await ctx.send(sender, create_text_chat(response, end_session=False))

    @chat_proto.on_message(ChatAcknowledgement)
    async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
        """Handle chat acknowledgements"""
        pass

    return chat_proto

