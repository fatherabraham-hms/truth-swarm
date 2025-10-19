# Testing Guide for DeFi Agent

## Quick Start Testing

### Step 1: Set up your environment

Make sure you have your `.env` file configured:

```bash
# Create .env file from the example
cp .env.example .env

# Edit with your OpenAI API key
nano .env
```

Your `.env` should contain:
```
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

### Step 2: Run the Main Agent

Open a terminal and run:

```bash
cd /home/akash/Hackathons/truth-swarm/Defi-tasks_agent
source venv/bin/activate  # Activate virtual environment
python Agent.py
```

You should see output like:
```
INFO:     [agent]: Starting agent with address: agent1q26a633p9cjduh42gt3mpflh34a2qgw3a0a46ca8xuthcu95qnd9vaevpsq
INFO:     [agent]: Starting server on http://0.0.0.0:8000
```

**Important**: Copy the agent address (starts with `agent1q...`) - you'll need this for testing!

### Step 3: Update Test Client with Agent Address

In another terminal, edit `test_client.py` and update line 14 with your agent's address:

```python
DEFI_AGENT_ADDRESS = "agent1q26a633p9cjduh42gt3mpflh34a2qgw3a0a46ca8xuthcu95qnd9vaevpsq"  # Use YOUR agent address
```

### Step 4: Run the Test Client

In the second terminal:

```bash
cd /home/akash/Hackathons/truth-swarm/Defi-tasks_agent
source venv/bin/activate
python test_client.py
```

You should see:
```
INFO:     [test_client]: Starting agent with address: agent1q2u6xwk2d35dw08jjmafx3vjj4sp4yzjjrcfmk9e5fnwy3w9fng8jhqwr7n
INFO:     [test_client]: Starting server on http://0.0.0.0:8001
```

The test client will automatically send a message every 5 seconds asking "What is yield farming?"

### Step 5: Check the Responses

Watch the **first terminal** (where Agent.py is running) for the responses. You should see the agent receiving messages and responding with information about yield farming.

## Fixed Issues ✅

1. ✅ **Port Conflict Fixed**: 
   - Main agent runs on port **8000**
   - Test client runs on port **8001**

2. ✅ **Deprecation Warning Fixed**: 
   - Changed from `datetime.utcnow()` to `datetime.now(UTC)`

3. ✅ **API Key Security**: 
   - Using environment variables instead of hardcoded keys

4. ✅ **Model Name Fixed**: 
   - Using `gpt-3.5-turbo` (valid model)

5. ✅ **Subject Matter Updated**: 
   - Changed from "birds" to DeFi topics

## Manual Testing Tips

### Test Different Questions

Edit `test_client.py` line 21 to ask different questions:

```python
TextContent(type="text", text="What is a liquidity pool?"),
# or
TextContent(type="text", text="Explain smart contracts"),
# or
TextContent(type="text", text="What is the weather?"),  # Should decline - not DeFi related
```

### Check API Usage

Monitor your OpenAI usage at: https://platform.openai.com/usage

### Stop the Agents

Press `Ctrl+C` in each terminal to stop the agents.

## Troubleshooting

### Still Getting Port Errors?

Check if anything is using the ports:
```bash
lsof -i :8000
lsof -i :8001
```

Kill any processes if needed:
```bash
kill -9 <PID>
```

### Not Receiving Messages?

1. Verify both agents are running
2. Check the agent address in test_client.py matches the one shown when Agent.py starts
3. Make sure both are on the same network/localhost

### OpenAI API Errors?

- Verify your API key is correct and active
- Check you have credits available in your OpenAI account
- Try switching to `gpt-4` if you have access (line 77 in Agent.py)

## Expected Behavior

**When working correctly:**

1. Main agent starts and listens on port 8000
2. Test client starts on port 8001
3. Test client sends a message every 5 seconds
4. Main agent receives the message
5. Main agent queries OpenAI API
6. Main agent sends back a response about DeFi
7. You see the conversation in the logs

## Alternative Testing: AgentVerse

You can also deploy and test on AgentVerse:

1. Go to https://agentverse.ai/
2. Create an account
3. Deploy your agent
4. Use the built-in chat interface

## Need Help?

- Check the main README.md for setup instructions
- Review error logs carefully
- Make sure all dependencies are installed: `pip install -r requirements.txt`

