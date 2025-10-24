# Crypto Detection Agent with meTTa Framework

A sophisticated AI agent that detects crypto-related agents using the meTTa symbolic reasoning framework and Agentverse integration for comprehensive agent analysis.

## 🚀 Features

- **meTTa Framework Integration**: Advanced symbolic reasoning using Hyperon/meTTa
- **Real-time Agent Detection**: Analyzes agents from Agentverse in real-time
- **Multi-source Analysis**: Evaluates README content, capabilities, and descriptions
- **Weighted Scoring**: Intelligent scoring based on source importance
- **REST API**: Complete REST API for agent interaction
- **Agentverse Integration**: Seamless integration with Agentverse ecosystem

## 📋 Prerequisites

- Python 3.9 (required for meTTa framework compatibility - Hyperon only supports Python 3.8-3.9)
- Git
- Agentverse API key

## 🛠️ Installation & Setup

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd truth-swarm/agents
```

### Step 2: Create Virtual Environment

Create a dedicated virtual environment for the meTTa framework:

**Important:** Hyperon (meTTa framework) only supports Python 3.8-3.9. If you don't have Python 3.9 installed:

**On macOS with Homebrew:**
```bash
# Install Python 3.9
brew install python@3.9

# Create virtual environment with Python 3.9
/opt/homebrew/bin/python3.9 -m venv venv-metta
```

**On Linux/Ubuntu:**
```bash
# Install Python 3.9
sudo apt update
sudo apt install python3.9 python3.9-venv

# Create virtual environment with Python 3.9
python3.9 -m venv venv-metta
```

**On Windows:**
```bash
# Download Python 3.9 from python.org and install
# Then create virtual environment
python3.9 -m venv venv-metta
```

**Activate the virtual environment:**
```bash
source venv-metta/bin/activate  # On macOS/Linux
# or
venv-metta\Scripts\activate     # On Windows
```

### Step 3: Install Dependencies

Install the required packages:

```bash
# Upgrade pip first
pip install --upgrade pip

# Install core dependencies
pip install uagents httpx python-dotenv

# Install meTTa framework (Hyperon) - requires Python 3.8-3.9
pip install hyperon

# Install additional dependencies
pip install pydantic fastapi uvicorn
```

**Note:** If you encounter an error installing `hyperon`, ensure you're using Python 3.9. The package is not available for Python 3.10+.

### Step 4: Set Up Environment Variables

Create a `.env` file in the agents directory:

```bash
# Create .env file
touch .env
```

Add your configuration:

```env
# Agentverse API Configuration
AGENTVERSE_API_KEY=your_api_key_here
AGENTVERSE_BASE_URL=https://agentverse.ai

# Agent Configuration
AGENT_NAME=crypto_detection_agent
AGENT_PORT=8000
```

**Getting Your Agentverse API Key:**
1. Go to [Agentverse](https://agentverse.ai)
2. Log in with your Gmail account
3. Navigate to Profile → API Keys
4. Create a new API key with appropriate permissions
5. Copy the key and paste it in your `.env` file

### Step 5: Verify meTTa Framework Installation

Test that the meTTa framework is properly installed:

```bash
python -c "from hyperon import GroundingSpace, S; print('✅ meTTa framework (Hyperon) installed successfully')"
```

Expected output:
```
✅ meTTa framework (Hyperon) installed successfully
```

## 🚀 Running the Agent

### Start the Agent

```bash
# Make sure you're in the agents directory
cd /path/to/truth-swarm/agents

# Activate the virtual environment
source venv-metta/bin/activate

# Start the agent
python run_agent.py
```

### Expected Output

When the agent starts successfully, you should see:

```
✅ meTTa framework (Hyperon) available
✅ meTTa framework (Hyperon) initialized successfully
✅ AgentVerse API client initialized
INFO: [crypto_detection_agent]: 🚀 Crypto Detection Agent started successfully!
INFO: [crypto_detection_agent]: 📍 Agent address: agent1q...
INFO: [crypto_detection_agent]: 🔧 Port: 8000
INFO: [crypto_detection_agent]: 🌐 Endpoint: http://localhost:8000
INFO: [crypto_detection_agent]: 🧠 meTTa Framework Status:
INFO: [crypto_detection_agent]:    Available: True
INFO: [crypto_detection_agent]:    Detector: Available
INFO: [crypto_detection_agent]:    Detection method: meTTa
INFO: [crypto_detection_agent]: 🌐 AgentVerse API Status:
INFO: [crypto_detection_agent]:    Available: True
INFO: [crypto_detection_agent]:    API Key: Set
INFO: [crypto_detection_agent]:    Base URL: https://agentverse.ai
INFO: [crypto_detection_agent]:    Profile reading: Enabled
INFO: [crypto_detection_agent]: 💡 Ready to detect crypto agents!
```

## 🧪 Testing the Agent

### Health Check

Test if the agent is running:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "agent_name": "crypto_detection_agent",
  "agent_address": "agent1q...",
  "uptime": "2025-10-24T17:22:05.834391+00:00",
  "metta_available": true,
  "agentverse_available": true,
  "version": "1.0.0"
}
```

### Crypto Detection Test

Test crypto detection on a specific agent:

```bash
curl -X POST http://localhost:8000/detect-crypto \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac"}'
```

Expected response for a crypto agent:
```json
{
  "agent_id": "agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac",
  "is_crypto_agent": true,
  "crypto_score": 0.64,
  "confidence": 0.7,
  "total_matches": 8,
  "readme_matches": [
    "crypto",
    "blockchain", 
    "defi",
    "decentralized",
    "token",
    "smart contract",
    "yield farming",
    "liquidity"
  ],
  "capability_matches": [],
  "description_matches": [],
  "evaluation_method": "metta",
  "processing_time": 0.17,
  "timestamp": "2025-10-24T17:22:05.834391+00:00"
}
```

### List Available Agents

Get a list of agents from Agentverse:

```bash
curl -X POST http://localhost:8000/list-agents \
  -H "Content-Type: application/json" \
  -d '{"limit": 10}'
```

## 🔧 API Endpoints

### Health Check
- **GET** `/health`
- Returns agent health status and configuration

### Crypto Detection
- **POST** `/detect-crypto`
- **Body**: `{"agent_id": "agent_address"}`
- Analyzes an agent for crypto-related content using meTTa framework

### List Agents
- **POST** `/list-agents`
- **Body**: `{"limit": 10, "offset": 0}`
- Returns a list of agents from Agentverse

### Discover Agents
- **POST** `/discover-agents`
- **Body**: `{"query": "search_term"}`
- Searches for agents on Agentverse

## 🧠 meTTa Framework Details

### How It Works

The meTTa framework provides advanced symbolic reasoning capabilities:

1. **Grounding Space**: Creates a symbolic knowledge base
2. **Weighted Analysis**: Different sources have different importance:
   - README content: 40% weight
   - Capabilities: 35% weight  
   - Description: 25% weight
3. **Multi-factor Confidence**: Considers:
   - Total keyword matches
   - Multi-source agreement
   - High-value keyword presence
4. **Enhanced Detection**: Finds crypto keywords like:
   - "crypto", "blockchain", "defi"
   - "decentralized", "token", "smart contract"
   - "yield farming", "liquidity", "nft"

### Detection Algorithm

```python
# Enhanced scoring using meTTa symbolic reasoning
readme_weight = 0.4    # README is most important
cap_weight = 0.35      # Capabilities are very important  
desc_weight = 0.25     # Description is less important

weighted_score = (readme_count * readme_weight + 
                cap_count * cap_weight + 
                desc_count * desc_weight)

crypto_score = min(1.0, weighted_score / 5.0)
is_crypto_agent = crypto_score > 0.3
```

## 🐛 Troubleshooting

### Common Issues

#### 1. meTTa Framework Not Available
```
⚠️ meTTa framework not available. Install with: pip install hyperon
```

**Solution:**
```bash
pip install hyperon
```

#### 2. Port Already in Use
```
ERROR: [Errno 48] error while attempting to bind on address ('0.0.0.0', 8000): [errno 48] address already in use
```

**Solution:**
```bash
# Kill processes using port 8000
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
```

#### 3. Agentverse API Connection Failed
```
WARNING: [crypto_detection_agent]: ⚠️ Agentverse connection failed
```

**Solutions:**
- Check your API key in the `.env` file
- Verify internet connection
- Ensure Agentverse service is available

#### 4. Python Version Issues
```
ERROR: Package requires Python >=3.12
```

**Solution:**
```bash
# Use Python 3.12 specifically
python3.12 -m venv venv-metta
source venv-metta/bin/activate
```

### Debug Mode

Enable debug logging by adding debug prints to see what data is being processed:

```python
# In detection/metta_detector.py
print(f"🔍 DEBUG: README content: {readme_content[:200]}...")
print(f"🔍 DEBUG: Matches found: {readme_matches}")
```

## 📁 Project Structure

```
agents/
├── detection/
│   ├── base_detector.py      # Base detection interface
│   ├── metta_detector.py     # meTTa framework detector
│   └── simple_detector.py    # Fallback simple detector
├── models/
│   └── data_models.py        # Pydantic data models
├── api/
│   └── agentverse_client.py  # Agentverse API client
├── utils/
│   └── crypto_keywords.py    # Crypto keyword definitions
├── meTTa_eval_agent_refactored.py  # Main agent implementation
├── run_agent.py              # Agent runner script
├── test_crypto_detection.py  # Test script
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🔄 Development Workflow

### Making Changes

1. **Edit Code**: Modify the agent implementation
2. **Restart Agent**: Kill and restart the agent process
3. **Test Changes**: Use the API endpoints to verify functionality
4. **Debug**: Check logs for any issues

### Testing New Features

```bash
# Test specific functionality
python test_crypto_detection.py

# Test with specific agent
curl -X POST http://localhost:8000/detect-crypto \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "your_test_agent_id"}'
```

## 📊 Performance Metrics

- **Processing Time**: ~0.17 seconds per detection
- **Accuracy**: High confidence with multi-factor analysis
- **Scalability**: Handles multiple concurrent requests
- **Memory Usage**: Efficient with Hyperon grounding space

## 🔧 Troubleshooting

### Common Issues

#### 1. Hyperon Installation Issues

**Problem:** `ERROR: Could not find a version that satisfies the requirement hyperon`

**Solution:** 
- Ensure you're using Python 3.9 (not 3.10+)
- Check your Python version: `python --version`
- If using Python 3.10+, create a new virtual environment with Python 3.9:
  ```bash
  # On macOS with Homebrew
  brew install python@3.9
  /opt/homebrew/bin/python3.9 -m venv venv-metta
  source venv-metta/bin/activate
  pip install hyperon
  ```

#### 2. meTTa Framework Not Available

**Problem:** `⚠️ meTTa framework not available`

**Solution:**
- Verify hyperon is installed: `python -c "import hyperon; print('OK')"`
- Check Python version compatibility
- Reinstall hyperon: `pip uninstall hyperon && pip install hyperon`

#### 3. AgentVerse API Connection Issues

**Problem:** `AgentVerse API not configured` or connection errors

**Solution:**
- Set your API key: `export AGENTVERSE_API_KEY="your_key_here"`
- Create `.env` file with your API key
- Verify API key is valid at [Agentverse](https://agentverse.ai)

#### 4. Port Already in Use

**Problem:** `Address already in use` on port 8000

**Solution:**
- Kill existing process: `lsof -ti:8000 | xargs kill -9`
- Or change port in `.env`: `AGENT_PORT=8001`

#### 5. Import Errors

**Problem:** `ModuleNotFoundError` for local modules

**Solution:**
- Ensure you're in the agents directory: `cd agents`
- Check virtual environment is activated: `which python`
- Install missing dependencies: `pip install -r requirements.txt`

### Debug Commands

```bash
# Check Python version
python --version

# Verify hyperon installation
python -c "from hyperon import Interpreter; print('✅ Hyperon OK')"

# Test meTTa framework
python -c "from hyperon import GroundingSpace, S; print('✅ meTTa OK')"

# Check environment variables
echo $AGENTVERSE_API_KEY

# Test agent startup
python run_agent.py
```

### Getting Help

1. Check the logs for detailed error messages
2. Verify all prerequisites are met
3. Test with the provided examples
4. Ensure Python 3.9 compatibility

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the logs for error messages
3. Verify your environment setup
4. Test with the provided examples

## 🎯 Next Steps

- [ ] Add more sophisticated meTTa reasoning patterns
- [ ] Implement agent clustering and categorization
- [ ] Add real-time monitoring dashboard
- [ ] Integrate with additional blockchain networks
- [ ] Add machine learning-based detection improvements

---

**Happy Agent Detection! 🚀**