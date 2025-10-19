from datetime import datetime, UTC
from uuid import uuid4
from uagents import Agent, Context
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    StartSessionContent,
    TextContent,
)

# Create a test client agent on a different port to avoid conflicts
test_agent = Agent(name="test_client", seed="test_client_seed", port=8001)

# The address of your DeFi agent (will be printed when you run Agent.py)
DEFI_AGENT_ADDRESS = "agent1q2u6xwk2d35dw08jjmafx3vjj4sp4yzjjrcfmk9e5fnwy3w9fng8jhqwr7n"  # Replace with actual address

@test_agent.on_interval(period=5.0, messages=ChatMessage)
async def send_message(ctx: Context):
    # Send a test message
    content = [
        StartSessionContent(type="start-session"),
        TextContent(type="text", text="What is yield farming?"),
    ]
    await ctx.send(
        DEFI_AGENT_ADDRESS,
        ChatMessage(timestamp=datetime.now(UTC), msg_id=uuid4(), content=content),
    )

if __name__ == "__main__":
    test_agent.run()