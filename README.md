# Truth Swarm

Truth Swarm is a verification mechanism for consumer protections in the age of agentic AI.

## Getting Started

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/truth-swarm.git
   cd truth-swarm
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   For development (includes testing and formatting tools):
   ```bash
   pip install -r requirements.txt
   ```
4. **Set environment variables**
   GET .env file vars from Abe   

## Running the Agent

1. **Navigate to the agents directory**
   ```bash
   cd src/agents
   ```

2. **Run the evaluator agent**
   ```bash
   python evaluator-agent.py
   ```

   The agent will start and be available at `http://localhost:8000`

## Project Structure

```
truth-swarm/
├── src/
│   └── agents/
│       └── evaluator-agent.py  # Main agent implementation
└── README.md
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
