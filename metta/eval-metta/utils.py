
import json
from openai import OpenAI
from .medicalrag import MedicalRAG
from .defirag import DefiRAG

class LLM:
    def __init__(self, api_key):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.asi1.ai/v1"
        )

    def create_completion(self, prompt, max_tokens=200):
        completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="asi1-mini",  # ASI:One model name
            max_tokens=max_tokens
        )
        return completion.choices[0].message.content

def get_intent_and_keyword(query, llm):
    """Use ASI:One API to classify intent and extract a keyword."""
    prompt = (
        f"Given the query: '{query}'\n"
        "Classify the intent as one of: 'symptom', 'treatment', 'side effect', 'faq', or 'unknown'.\n"
        "Extract the most relevant keyword (e.g., a symptom, disease, or treatment) from the query.\n"
        "Return *only* the result in JSON format like this, with no additional text:\n"
        "{\n"
        "  \"intent\": \"<classified_intent>\",\n"
        "  \"keyword\": \"<extracted_keyword>\"\n"
        "}"
    )
    response = llm.create_completion(prompt)
    try:
        result = json.loads(response)
        return result["intent"], result["keyword"]
    except json.JSONDecodeError:
        print(f"Error parsing ASI:One response: {response}")
        return "unknown", None

def generate_knowledge_response(query, intent, keyword, llm):
    """Use ASI:One to generate a response for new knowledge based on intent."""
    if intent == "symptom":
        prompt = (
            f"Query: '{query}'\n"
            "The symptom '{keyword}' is not in my knowledge base. Suggest a plausible disease it might be linked to.\n"
            "Return *only* the disease name, no additional text."
        )
    elif intent == "treatment":
        prompt = (
            f"Query: '{query}'\n"
            "The disease or condition '{keyword}' has no known treatments in my knowledge base. Suggest a plausible treatment.\n"
            "Return *only* the treatment description, no additional text."
        )
    elif intent == "side effect":
        prompt = (
            f"Query: '{query}'\n"
            "The treatment '{keyword}' has no known side effects in my knowledge base. Suggest plausible side effects.\n"
            "Return *only* the side effects description, no additional text."
        )
    elif intent == "faq":
        prompt = (
            f"Query: '{query}'\n"
            "This is a new FAQ not in my knowledge base. Provide a concise, helpful answer.\n"
            "Return *only* the answer, no additional text."
        )
    else:
        return None
    return llm.create_completion(prompt)

def process_query(query, rag: MedicalRAG, llm: LLM):
    intent, keyword = get_intent_and_keyword(query, llm)
    print(f"Intent: {intent}, Keyword: {keyword}")
    prompt = ""

    if intent == "faq":
        faq_answer = rag.query_faq(query)
        if not faq_answer and keyword:
            new_answer = generate_knowledge_response(query, intent, keyword, llm)
            rag.add_knowledge("faq", query, new_answer)
            print(f"Knowledge graph updated - Added FAQ: '{query}' → '{new_answer}'")
            prompt = (
                f"Query: '{query}'\n"
                f"FAQ Answer: '{new_answer}'\n"
                "Humanize this for a medical assistant with a friendly tone."
            )
        elif faq_answer:
            prompt = (
                f"Query: '{query}'\n"
                f"FAQ Answer: '{faq_answer}'\n"
                "Humanize this for a medical assistant with a friendly tone."
            )
    elif intent == "symptom" and keyword:
        diseases = rag.query_symptom(keyword)
        if not diseases:
            disease = generate_knowledge_response(query, intent, keyword, llm)
            rag.add_knowledge("symptom", keyword, disease)
            print(f"Knowledge graph updated - Added symptom: '{keyword}' → '{disease}'")
            treatments = rag.get_treatment(disease) or ["rest, consult a doctor"]
            side_effects = [rag.get_side_effects(t) for t in treatments] if treatments else []
            prompt = (
                f"Query: '{query}'\n"
                f"Symptom: {keyword}\n"
                f"Related Disease: {disease}\n"
                f"Treatments: {', '.join(treatments)}\n"
                f"Side Effects: {', '.join([', '.join(se) for se in side_effects if se])}\n"
                "Generate a concise, empathetic response for a medical assistant."
            )
        else:
            disease = diseases[0]
            treatments = rag.get_treatment(disease)
            side_effects = [rag.get_side_effects(t) for t in treatments] if treatments else []
            prompt = (
                f"Query: '{query}'\n"
                f"Symptom: {keyword}\n"
                f"Related Disease: {disease}\n"
                f"Treatments: {', '.join(treatments)}\n"
                f"Side Effects: {', '.join([', '.join(se) for se in side_effects if se])}\n"
                "Generate a concise, empathetic response for a medical assistant."
            )
    elif intent == "treatment" and keyword:
        treatments = rag.get_treatment(keyword)
        if not treatments:
            treatment = generate_knowledge_response(query, intent, keyword, llm)
            rag.add_knowledge("treatment", keyword, treatment)
            print(f"Knowledge graph updated - Added treatment: '{keyword}' → '{treatment}'")
            prompt = (
                f"Query: '{query}'\n"
                f"Disease: {keyword}\n"
                f"Treatments: {treatment}\n"
                "Provide a helpful treatment suggestion."
            )
        else:
            prompt = (
                f"Query: '{query}'\n"
                f"Disease: {keyword}\n"
                f"Treatments: {', '.join(treatments)}\n"
                "Provide a helpful treatment suggestion."
            )
    elif intent == "side effect" and keyword:
        side_effects = rag.get_side_effects(keyword)
        if not side_effects:
            side_effect = generate_knowledge_response(query, intent, keyword, llm)
            rag.add_knowledge("side_effect", keyword, side_effect)
            print(f"Knowledge graph updated - Added side effect: '{keyword}' → '{side_effect}'")
            prompt = (
                f"Query: '{query}'\n"
                f"Treatment: {keyword}\n"
                f"Side Effects: {side_effect}\n"
                "Provide a concise explanation of side effects."
            )
        else:
            prompt = (
                f"Query: '{query}'\n"
                f"Treatment: {keyword}\n"
                f"Side Effects: {', '.join(side_effects)}\n"
                "Provide a concise explanation of side effects."
            )
    
    if not prompt:
        prompt = f"Query: '{query}'\nNo specific info found. Offer general assistance."

    prompt += "\nFormat response as: 'Selected Question: <question>' on first line, 'Humanized Answer: <response>' on second."
    response = llm.create_completion(prompt)
    try:
        selected_q = response.split('\n')[0].replace("Selected Question: ", "").strip()
        answer = response.split('\n')[1].replace("Humanized Answer: ", "").strip()
        return {"selected_question": selected_q, "humanized_answer": answer}
    except IndexError:
        return {"selected_question": query, "humanized_answer": response}

# ========================================
# DEFI-SPECIFIC FUNCTIONS
# ========================================

def get_defi_intent_and_keyword(query, llm):
    """
    Use ASI:One API to classify DeFi intent and extract a keyword.
    
    Intents: 'protocol_query', 'operation', 'constraint', 'risk', 'asset', 'faq', 'unknown'
    """
    prompt = (
        f"Given the DeFi query: '{query}'\n"
        "Classify the intent as one of: 'protocol_query', 'operation', 'constraint', 'risk', 'asset', 'faq', or 'unknown'.\n"
        "- 'protocol_query': asking about what a protocol can do (e.g., 'What can I do on Uniswap?')\n"
        "- 'operation': asking about specific operations (e.g., 'How do I swap tokens?', 'What is required to borrow?')\n"
        "- 'constraint': asking about limits/rules (e.g., 'What is max slippage?', 'What are safe leverage ratios?')\n"
        "- 'risk': asking about risks/security (e.g., 'What are the risks of swapping?', 'Is this safe?')\n"
        "- 'asset': asking about tokens/assets (e.g., 'Is USDC stable?', 'What type is ETH?')\n"
        "- 'faq': general DeFi questions (e.g., 'What is slippage?', 'What is MEV?')\n"
        "Extract the most relevant keyword (protocol name, operation, asset symbol, or topic).\n"
        "Return *only* the result in JSON format like this, with no additional text:\n"
        "{\n"
        "  \"intent\": \"<classified_intent>\",\n"
        "  \"keyword\": \"<extracted_keyword>\"\n"
        "}"
    )
    response = llm.create_completion(prompt)
    try:
        result = json.loads(response)
        return result["intent"], result["keyword"]
    except json.JSONDecodeError:
        print(f"Error parsing ASI:One response: {response}")
        return "unknown", None

def generate_defi_knowledge_response(query, intent, keyword, llm):
    """Use ASI:One to generate a response for new DeFi knowledge based on intent."""
    if intent == "protocol_query":
        prompt = (
            f"Query: '{query}'\n"
            f"The protocol '{keyword}' is not in my knowledge base. Suggest plausible operations it might support.\n"
            "Return *only* comma-separated operation names, no additional text."
        )
    elif intent == "operation":
        prompt = (
            f"Query: '{query}'\n"
            f"The operation '{keyword}' has no details in my knowledge base. Suggest required parameters for this DeFi operation.\n"
            "Return *only* comma-separated parameter names, no additional text."
        )
    elif intent == "constraint":
        prompt = (
            f"Query: '{query}'\n"
            f"No constraints found for '{keyword}'. Suggest appropriate DeFi constraints (e.g., slippage limits, leverage ratios).\n"
            "Return *only* the constraint in format 'constraint_type:value', no additional text."
        )
    elif intent == "risk":
        prompt = (
            f"Query: '{query}'\n"
            f"No risks documented for '{keyword}'. Identify plausible DeFi/security risks.\n"
            "Return *only* the risk description, no additional text."
        )
    elif intent == "asset":
        prompt = (
            f"Query: '{query}'\n"
            f"The asset '{keyword}' classification is unknown. Is it a stablecoin, volatile asset, or LST?\n"
            "Return *only* 'stable', 'volatile', or 'lst', no additional text."
        )
    elif intent == "faq":
        prompt = (
            f"Query: '{query}'\n"
            "This is a new DeFi FAQ not in my knowledge base. Provide a concise, accurate answer.\n"
            "Return *only* the answer, no additional text."
        )
    else:
        return None
    return llm.create_completion(prompt)

def process_defi_query(query, rag: DefiRAG, llm: LLM):
    """
    Process a DeFi query using DefiRAG and LLM.
    
    This function demonstrates how to use the DeFi knowledge graph for
    answering queries and can be extended for agent evaluation.
    
    Args:
        query: User query string
        rag: DefiRAG instance
        llm: LLM instance
        
    Returns:
        Dict with selected_question and humanized_answer
    """
    intent, keyword = get_defi_intent_and_keyword(query, llm)
    print(f"[DeFi] Intent: {intent}, Keyword: {keyword}")
    prompt = ""

    if intent == "faq":
        faq_answer = rag.query_faq(query)
        if not faq_answer and keyword:
            new_answer = generate_defi_knowledge_response(query, intent, keyword, llm)
            rag.add_knowledge("faq", query, new_answer)
            print(f"Knowledge graph updated - Added FAQ: '{query}' → '{new_answer}'")
            prompt = (
                f"Query: '{query}'\n"
                f"FAQ Answer: '{new_answer}'\n"
                "Humanize this for a DeFi assistant with a helpful, clear tone."
            )
        elif faq_answer:
            prompt = (
                f"Query: '{query}'\n"
                f"FAQ Answer: '{faq_answer}'\n"
                "Humanize this for a DeFi assistant with a helpful, clear tone."
            )
    
    elif intent == "protocol_query" and keyword:
        operations = rag.query_protocol_operations(keyword)
        if not operations:
            ops_suggestion = generate_defi_knowledge_response(query, intent, keyword, llm)
            rag.add_knowledge("protocol", keyword, ops_suggestion)
            print(f"Knowledge graph updated - Added protocol: '{keyword}' → '{ops_suggestion}'")
            prompt = (
                f"Query: '{query}'\n"
                f"Protocol: {keyword}\n"
                f"Supported Operations: {ops_suggestion}\n"
                "Generate a helpful response about what this protocol can do."
            )
        else:
            # Get additional context for each operation
            operation_details = []
            for op in operations[:3]:  # Limit to first 3 for brevity
                constraints = rag.get_operation_constraints(op)
                risks = rag.get_operation_risks(op)
                operation_details.append({
                    "operation": op,
                    "constraints": constraints[:2] if constraints else [],
                    "risks": risks[:1] if risks else []
                })
            
            prompt = (
                f"Query: '{query}'\n"
                f"Protocol: {keyword}\n"
                f"Supported Operations: {', '.join(operations)}\n"
                f"Operation Details: {json.dumps(operation_details, indent=2)}\n"
                "Generate a comprehensive response about this protocol's capabilities, "
                "mentioning key operations and any important constraints or risks."
            )
    
    elif intent == "operation" and keyword:
        # Get comprehensive operation info
        op_info = rag.get_comprehensive_operation_info(keyword)
        
        if not op_info["protocols"] and not op_info["requirements"]:
            # No knowledge about this operation
            new_info = generate_defi_knowledge_response(query, intent, keyword, llm)
            rag.add_knowledge("requires", keyword, new_info)
            print(f"Knowledge graph updated - Added operation requirements: '{keyword}' → '{new_info}'")
            prompt = (
                f"Query: '{query}'\n"
                f"Operation: {keyword}\n"
                f"Requirements: {new_info}\n"
                "Explain this DeFi operation and its requirements."
            )
        else:
            prompt = (
                f"Query: '{query}'\n"
                f"Operation: {keyword}\n"
                f"Supported by Protocols: {', '.join(op_info['protocols']) if op_info['protocols'] else 'multiple protocols'}\n"
                f"Required Parameters: {', '.join(op_info['requirements']) if op_info['requirements'] else 'none specified'}\n"
                f"Constraints: {', '.join(op_info['constraints']) if op_info['constraints'] else 'none specified'}\n"
                f"Risks: {', '.join(op_info['risks']) if op_info['risks'] else 'none documented'}\n"
                f"Best Practices: {', '.join(op_info['best_practices']) if op_info['best_practices'] else 'none documented'}\n"
                "Generate a comprehensive explanation of this operation, including requirements, "
                "constraints, risks, and best practices. Be clear and educational."
            )
    
    elif intent == "constraint" and keyword:
        # Determine if keyword is an operation or parameter
        constraints = rag.get_operation_constraints(keyword)
        
        if not constraints:
            new_constraint = generate_defi_knowledge_response(query, intent, keyword, llm)
            rag.add_knowledge("constraint", keyword, new_constraint)
            print(f"Knowledge graph updated - Added constraint: '{keyword}' → '{new_constraint}'")
            prompt = (
                f"Query: '{query}'\n"
                f"Topic: {keyword}\n"
                f"Constraint: {new_constraint}\n"
                "Explain this DeFi constraint and why it's important."
            )
        else:
            parsed_constraints = [rag.parse_constraint(c) for c in constraints]
            prompt = (
                f"Query: '{query}'\n"
                f"Topic: {keyword}\n"
                f"Constraints: {json.dumps(parsed_constraints, indent=2)}\n"
                "Explain these DeFi constraints, their purposes, and recommended safe values."
            )
    
    elif intent == "risk" and keyword:
        risks = rag.get_operation_risks(keyword)
        best_practices = rag.get_best_practices(keyword)
        
        if not risks:
            new_risk = generate_defi_knowledge_response(query, intent, keyword, llm)
            rag.add_knowledge("risk", keyword, new_risk)
            print(f"Knowledge graph updated - Added risk: '{keyword}' → '{new_risk}'")
            prompt = (
                f"Query: '{query}'\n"
                f"Topic: {keyword}\n"
                f"Risks: {new_risk}\n"
                "Explain these risks and how to mitigate them."
            )
        else:
            prompt = (
                f"Query: '{query}'\n"
                f"Topic: {keyword}\n"
                f"Risks: {', '.join(risks)}\n"
                f"Best Practices: {', '.join(best_practices) if best_practices else 'none documented'}\n"
                "Explain these DeFi risks clearly and provide actionable mitigation strategies."
            )
    
    elif intent == "asset" and keyword:
        asset_type = rag.query_asset_type(keyword)
        
        if not asset_type:
            new_type = generate_defi_knowledge_response(query, intent, keyword, llm)
            rag.add_knowledge("asset-type", keyword, new_type)
            print(f"Knowledge graph updated - Added asset type: '{keyword}' → '{new_type}'")
            prompt = (
                f"Query: '{query}'\n"
                f"Asset: {keyword}\n"
                f"Type: {new_type}\n"
                "Explain this asset's characteristics and risk profile."
            )
        else:
            # Provide context based on asset type
            type_descriptions = {
                "stable": "stablecoin (low volatility, pegged to fiat)",
                "volatile": "volatile crypto asset (high price variability)",
                "lst": "liquid staking token (staked asset with DeFi utility)"
            }
            description = type_descriptions.get(asset_type, asset_type)
            
            prompt = (
                f"Query: '{query}'\n"
                f"Asset: {keyword}\n"
                f"Type: {description}\n"
                "Explain this asset type, its characteristics, and appropriate use cases in DeFi."
            )
    
    if not prompt:
        prompt = f"Query: '{query}'\nNo specific DeFi info found. Offer general DeFi assistance."

    prompt += "\nFormat response as: 'Selected Question: <question>' on first line, 'Humanized Answer: <response>' on second."
    response = llm.create_completion(prompt)
    try:
        selected_q = response.split('\n')[0].replace("Selected Question: ", "").strip()
        answer = response.split('\n')[1].replace("Humanized Answer: ", "").strip()
        return {"selected_question": selected_q, "humanized_answer": answer}
    except IndexError:
        return {"selected_question": query, "humanized_answer": response}

# ========================================
# EVALUATION SCORING FUNCTIONS
# ========================================

def calculate_evaluation_score(metric_scores):
    """
    Calculate final evaluation score based on multiple metric scores.
    
    Implements the axiom: "Confident but wrong is worse than low-confidence that is right"
    
    Args:
        metric_scores: Dict of {metric_name: {score, confidence, evidence, failures}}
        
    Returns:
        Final attestation object ready for signing
    """
    weights = {
        "capability": 0.15,
        "functional": 0.20,
        "domain": 0.20,
        "operational": 0.15,
        "security": 0.20,
        "robustness": 0.05,
        "explainability": 0.05
    }
    
    effective_scores = {}
    for metric, data in metric_scores.items():
        score = data['score']
        confidence = data['confidence']
        
        # Axiom implementation: penalize high confidence + low score
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
        effective_scores.get(metric, 0) * weight
        for metric, weight in weights.items()
    )
    
    # Overall confidence: weighted average of individual confidences
    overall_confidence = sum(
        metric_scores.get(metric, {}).get('confidence', 0) * weight
        for metric, weight in weights.items()
    )
    
    # Grade assignment
    if final_score >= 90:
        grade = "A"
    elif final_score >= 80:
        grade = "B"
    elif final_score >= 70:
        grade = "C"
    elif final_score >= 60:
        grade = "D"
    else:
        grade = "F"
    
    return {
        "evaluator": "truth-swarm-metta-v1",
        "timestamp": None,  # Should be set by caller
        "final_score": round(final_score, 2),
        "overall_confidence": round(overall_confidence, 2),
        "grade": grade,
        "metrics": metric_scores,
        "effective_scores": {k: round(v, 2) for k, v in effective_scores.items()},
        "weights": weights,
        "attestation_version": "1.0.0"
    }