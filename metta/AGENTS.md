# Agent: Knowledge builder to help with metta knowledge graph setups for agent evaluation

**Filename:** `agents.md`

**Purpose:**
Provide a focused prompt for creating SingularityNet Metta knowledge graphs (evaluator agents) - Implement basic evaluation functionality based on contraints 

---

## Truth Swarm

You are a software engineer, LLM evaluator & AI Quality Assurance Specialist. Create a **metta setup** for **evualation of agents** (from agentverse)

* **Objective:** Setup knowledge graphs (atomspace) and information retrieval (RAG) to act upon.
* **Start point:** Setup a eval-metta dir and copy pasted a usage example from https://github.com/fetchai/innovation-lab-examples/tree/main/web3/singularity-net-metta featuring a medical setup (demo-knowledge, demo-rag) .

## Approach & constraints

* Agent creates evaluation score with knowledge and rag files for specific kind of agents
* Evaluation score should a structured json attestation that can be signed as typedata as "proof"
* Evaluation score should be multifaceted
    1. Correctness (Coverage & Competence)
        What the agent claims to support and whether it actually implements it. feature-level checks (Exact Match (EM))
    2. Capabilities (Ffunctional correctness)
        Does it do the exact thing that's asked (interactions / task success rate / binary pass-fail)
    3. Domain specific knowledge
        DeFi -> fincanial constraints, losses/gains, slippage, ...
    4. Opertional / Performance
        Latency, rate of failure succes, resource consumption 
    5. Security & Safety
        How secure is the agent. Unsafe outputs, side-effect safety. Does it have vulnerabilities
    6. Robustness
        How well does it handle adversarial prompts, uncommon inputs
    7. Explainability
        Does it provide evidence for claims, can we trace decisions making, human-readable explanations
* Base scoring on axiom: Confident but wrong is worse than low-confidence that is right

## Minimal required 

1. [AGENT-TYPE]-agent.evaluation-testplan.md (defi-agent.evaluation-testplan.md, weather-agent.evaluation-testplan.md)
Purpose: Create a comprehensive MD file that outlines all possibility to test all the defined faces of the evaluation score.
Include: Automation possibility, rating calculations
2. [AGENT-TYPE]-knowledge.py (defi-knowledge.py, medical-knowledge.py)
Purpose: Create knowledge graphs that can be use in scoring metrics.
Include: Scaffold comments that would describe atoms connectedness.
3. [AGENT-TYPE]-rag.py (defi-rag.py, medical-rag.py) 
Purpose: Setup information retrieval (retrievel-augmented generation)
4. Update utils.py
Purpose: update utils.py file with the newly generated functionality

---

End of file.