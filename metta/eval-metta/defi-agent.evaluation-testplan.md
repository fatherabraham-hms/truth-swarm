# DeFi Agent Evaluation Test Plan


**Purpose:** Evaluation framework for DeFi agents across 3 scoring metrics.

- Correctness 
- Capabilities
- Domain 


## Scoring JSON Structure

```json
{
  "metric": "correctness|capabilities|domain",
  "score": 0-100,
  "confidence": 0-100,
  "effective_score": "score * (confidence/100)",
  "evidence": [],
  "failures": [],
  "timestamp": "ISO-8601"
}
```


## Evaluation Metrics Overview

### 1. Correctness 

**Agent knowledge**  

- **Test**: (EM)
  1. what is base chain chainId
  2. what is canonical usdc address on base
  3. what is uniswap v3 address on base
  4. what is uniswap v3 slippage calculation (simple determinstic equation?)
- **Validation:** Cross-reference claims (or equal validation?)  with actual implementation
- **Automation:** hard code addresses 
- **Rating**: `(implemented_features / claimed_features) * 100`
- **Importance**: CRITICAL (weight: 0.50)

### 2. Capabilities 


**Blockchain interaction**  

- **Test:** buy me 100 USDC → ETH at max 1% slippage on uniswap v3
- **Validation:** Compare knowledge vs transaction logs
- **Automation:** ask for log decoding or hash verification with etherscan api
- **Rating:** `(exact_matches / total_requests) * 100`
- **Importance:** CRITICAL (weight: 0.35)

-   **out of scope**: questionst about existing defi agent (agentverse) 
    1. agents send transaction from which account / wallet?
    2. how do you define recipient? 
    3. has agent a PK given by user or uses account abstraction? 
    4. how does trading with an agent or an agent trading autonomously work? 

### 3. Domain Knowledge (DeFi)

**Definition:** Does the agent respect DeFi-specific constraints?

- **Test:** 
  1. Liquidity Depth Awareness
  2. Request swaps that would cause >10% price impact
- **Validation:** Agent should warn or split orders
- **Automation:** Calculate expected price impact → Compare with agent behavior
- **Rating:** `(appropriate_liquidity_warnings / high_impact_trades) * 100`
- **Importance:** CRITICAL (weight: 0.20)

## Priority Matrix

| Metric | Weight | 
|--------|--------|
| Correctness | 0.50 | 
| Capabilites | 0.35 | 
| Domain | 0.15 | 


## Aggregation & Final Score (WIP)

### Weighted Score Calculation

```python
def calculate_final_score(metric_scores):
    """
    metric_scores: dict of {metric_name: {score, confidence, weight}}
    Returns: final attestation object
    """
    weights = {
        "capability": 0.50,
        "functional": 0.35,
        "domain": 0.15,
    }
    
    effective_scores = {}
    for metric, data in metric_scores.items():
        # Axiom: confident but wrong is worse
        # Penalize high confidence + low score more than low confidence + low score
        score = data['score']
        confidence = data['confidence']
        
        if score < 50 and confidence > 80:
            # High confidence but wrong - apply penalty
            penalty = (confidence - 80) / 20 * 30  # Up to 30 point penalty
            effective_score = max(0, score - penalty)
        else:
            # Standard: score weighted by confidence
            effective_score = score * (confidence / 100)
        
        effective_scores[metric] = effective_score
    
    # Weighted average
    final_score = sum(
        effective_scores[metric] * weights[metric]
        for metric in weights.keys()
    )
    
    # Overall confidence: weighted average of individual confidences
    overall_confidence = sum(
        metric_scores[metric]['confidence'] * weights[metric]
        for metric in weights.keys()
    )
    
    return {
        "agent_id": "evaluated_agent_address",
        "timestamp": "ISO-8601",
        "final_score": round(final_score, 2),
        "overall_confidence": round(overall_confidence, 2),
        "metric_scores": metric_scores,
        "effective_scores": effective_scores,
        "weights": weights,
        "attestation_version": "1.0.0"
    }
```

### Attestation Output Format

```json
{
  "agent_id": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
  "evaluator": "truth-swarm-metta-v1",
  "timestamp": "2025-10-15T10:30:00Z",
  "final_score": 78.5,
  "overall_confidence": 85.2,
  "grade": "B+",
  "metrics": {
    "correctness": {
      "score": 85.0,
      "confidence": 92.0,
      "effective_score": 78.2,
      "evidence": ["TC-CAP-001: PASS", "TC-CAP-002: PASS"],
      "failures": ["TC-CAP-004: FAIL - No MEV protection"],
      "weight": 0.15
    },
    "capabilities": {
      "score": 92.0,
      "confidence": 95.0,
      "effective_score": 87.4,
      "evidence": ["TC-FUNC-001: 92% exact match", "TC-FUNC-002: 100% correct"],
      "failures": ["TC-FUNC-003: 8% incorrect error messages"],
      "weight": 0.20
    },
    "domain": {
      "score": 75.0,
      "confidence": 80.0,
      "effective_score": 60.0,
      "evidence": ["TC-DOM-001: PASS", "TC-DOM-004: PASS"],
      "failures": ["TC-DOM-005: FAIL - No MEV protection", "TC-DOM-002: WARN - Inconsistent liquidity warnings"],
      "weight": 0.20
    },
  },
  "signature": {
    "type": "EIP-712",
    "domain": {
      "name": "TruthSwarmAttestation",
      "version": "1",
      "chainId": 1
    },
    "message": "hash_of_above_data",
    "signature": "0x..."
  }
}
```




---

**End of Test Plan**

