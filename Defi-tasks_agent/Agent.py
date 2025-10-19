
import os
from datetime import datetime, UTC
from uuid import uuid4

from openai import OpenAI
from uagents import Context, Protocol, Agent
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

##
### Example Expert Assistant
##
## This chat example is a barebones example of how you can create a simple chat agent
## and connect to agentverse. In this example we will be prompting the ASI-1 model to
## answer questions on a specific subject only.
##

def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(timestamp=datetime.now(UTC), msg_id=uuid4(), content=content)

# the subject that this assistant is an expert in
subject_matter = "DeFi (Decentralized Finance), blockchain protocols, smart contracts, yield farming, liquidity pools, and cryptocurrency trading"

# Knowledge base for common DeFi questions
QA_MAP = {
    "what is base chain chainid": "8453",  # Example chainId for Base chain
    "what is canonical usdc address on base": "0x7F5c764cBc14f9669B88837ca1490cCa17c31607",
    "what is uniswap v3 address on base": "0x1F98431c8aD98523631AE4a59f267346ea31F984",
    "what is uniswap v3 slippage calculation": "Slippage = (Price Impact Percentage). For example: Slippage = |Expected Price - Actual Price| / Expected Price"
}

def find_answer_in_knowledge_base(question: str) -> str | None:
    """
    Check if the question matches any entry in the knowledge base.
    Returns the answer if found, None otherwise.
    """
    normalized_question = question.lower().strip().rstrip('?').rstrip('.')
    
    # Direct match
    if normalized_question in QA_MAP:
        return QA_MAP[normalized_question]
    
    # Fuzzy matching - check if question contains key phrases
    for key, value in QA_MAP.items():
        if key in normalized_question or normalized_question in key:
            return value
    
    return None

# Get API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please create a .env file with your API key.")

client = OpenAI(
    base_url='https://api.openai.com/v1',
    api_key=api_key,
)

agent = Agent()

# We create a new protocol which is compatible with the chat protocol spec. This ensures
# compatibility between agents
protocol = Protocol(spec=chat_protocol_spec)


# We define the handler for the chat messages that are sent to your agent
@protocol.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    # send the acknowledgement for receiving the message
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.now(), acknowledged_msg_id=msg.msg_id),
    )

    # 2) greet if a session starts
    if any(isinstance(item, StartSessionContent) for item in msg.content):
        await ctx.send(
            sender,
            create_text_chat(f"Hi! Im a {subject_matter} expert, how can I help?", end_session=False),
        )

    text = msg.text()
    if not text:
        return

    # First check if the answer is in our knowledge base
    kb_answer = find_answer_in_knowledge_base(text)
    if kb_answer:
        ctx.logger.info(f"Found answer in knowledge base for: {text}")
        await ctx.send(sender, create_text_chat(kb_answer, end_session=True))
        return

    # If not in knowledge base, use OpenAI API
    try:
        # Include knowledge base context in the system prompt
        kb_context = "\n\nYou also have access to this specific knowledge:\n"
        for question, answer in QA_MAP.items():
            kb_context += f"- {question}: {answer}\n"
        
        r = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use gpt-4 or gpt-4-turbo for better responses
            messages=[
                {"role": "system", "content": f"""You are a helpful assistant who only answers questions about {subject_matter}. If the user asks about any other topics, you should politely say that you do not know about them.{kb_context}"""},
                {"role": "user", "content": text},
            ],
            max_tokens=2048,
        )

        response = str(r.choices[0].message.content)
    except Exception as e:
        ctx.logger.exception('Error querying model')
        response = f"An error occurred while processing the request. Please try again later. {e}"

    await ctx.send(sender, create_text_chat(response, end_session=True))


@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    # we are not interested in the acknowledgements for this example, but they can be useful to
    # implement read receipts, for example.
    pass


# attach the protocol to the agent
agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
    