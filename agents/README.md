# DeFi Evaluator Agent

This guide explains how to set up and run the DeFi Evaluator Agent, its backend components, and the user interface.

## Instructions

Follow these steps to run the full application stack.

### 1. Start the Evaluator Agent

This command starts the main agent, which listens for evaluation requests.

```bash
python agents/evaluator_agent.py
```

### 2. Start the Backend API

This service seems to be a helper for the frontend. Run it in a separate terminal.

```bash
uvicorn agents.evaluator_agent:app --port 9000 --reload
```

### 3. Start the Frontend

Navigate to the UI directory and start the development server.

```bash
# Navigate to the UI directory (only for the first time)
cd ui

# Install dependencies (if you haven't already)
npm install

# Start the frontend application
npm run dev
```

### 4. Using the Application

Once all services are running:
- Open your web browser to the frontend URL (usually `http://localhost:5173`).
- Enter the address of the agent you want to evaluate.
- Press Enter to submit the request.
- The evaluation results will be displayed on the page.