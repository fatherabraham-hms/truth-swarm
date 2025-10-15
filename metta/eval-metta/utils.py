
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
    Use ASI:One API to classify DeFi intent and extract a keyword (MVP version).
    
    Intents: 'chain_info', 'address', 'formula', 'swap', 'constraint', 'unknown'
    """
    prompt = (
        f"Given the DeFi query: '{query}'\n"
        "Classify the intent as one of: 'chain_info', 'address', 'formula', 'swap', 'constraint', or 'unknown'.\n"
        "- 'chain_info': asking about blockchain info (e.g., 'What is Base chain ID?')\n"
        "- 'address': asking about token or protocol addresses (e.g., 'What is USDC address on Base?')\n"
        "- 'formula': asking about calculations (e.g., 'How to calculate slippage?')\n"
        "- 'swap': asking about swap operations (e.g., 'Buy USDC to ETH', 'How to swap on Uniswap?')\n"
        "- 'constraint': asking about limits (e.g., 'What is max price impact?')\n"
        "Extract the most relevant keyword.\n"
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
    """Use ASI:One to generate a response for new DeFi knowledge based on intent (MVP version)."""
    if intent == "chain_info":
        prompt = (
            f"Query: '{query}'\n"
            f"Provide the chain ID for '{keyword}' blockchain.\n"
            "Return *only* the chain ID number, no additional text."
        )
    elif intent == "address":
        prompt = (
            f"Query: '{query}'\n"
            f"Provide the canonical address for '{keyword}' on the specified blockchain.\n"
            "Return *only* the Ethereum address (0x...), no additional text."
        )
    elif intent == "formula":
        prompt = (
            f"Query: '{query}'\n"
            f"Provide the formula for calculating '{keyword}' in DeFi.\n"
            "Return *only* the formula as a simple equation, no additional text."
        )
    elif intent == "swap":
        prompt = (
            f"Query: '{query}'\n"
            "Provide required parameters for executing a token swap.\n"
            "Return *only* comma-separated parameter names, no additional text."
        )
    elif intent == "constraint":
        prompt = (
            f"Query: '{query}'\n"
            f"Provide the maximum safe limit for '{keyword}' in DeFi swaps.\n"
            "Return *only* a percentage value, no additional text."
        )
    else:
        return None
    return llm.create_completion(prompt)

def process_defi_query(query, rag: DefiRAG, llm: LLM):
    """
    Process a DeFi query using DefiRAG and LLM (MVP version).
    
    Supports 3 evaluation metrics:
    - Correctness: Chain info, addresses, formulas
    - Capabilities: Swap operations
    - Domain: Price impact constraints
    
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

    if intent == "chain_info" and keyword:
        # CORRECTNESS METRIC: Query blockchain information
        chain_info = rag.query_chain_info(keyword)
        if chain_info:
            prompt = (
                f"Query: '{query}'\n"
                f"Chain: {keyword}\n"
                f"Info: {chain_info}\n"
                "Provide a clear answer about this blockchain information."
            )
        else:
            prompt = f"Query: '{query}'\nNo chain information found for '{keyword}'."
    
    elif intent == "address" and keyword:
        # CORRECTNESS METRIC: Query token/protocol addresses
        # Try token address first
        token_address = rag.query_token_address(keyword)
        protocol_address = rag.query_protocol_address(keyword)
        
        if token_address or protocol_address:
            address = token_address or protocol_address
            prompt = (
                f"Query: '{query}'\n"
                f"Item: {keyword}\n"
                f"Address: {address}\n"
                "Provide the requested address clearly."
            )
        else:
            prompt = f"Query: '{query}'\nNo address found for '{keyword}'."
    
    elif intent == "formula" and keyword:
        # CORRECTNESS METRIC: Query calculation formulas
        formula = rag.query_formula(keyword)
        if formula:
            prompt = (
                f"Query: '{query}'\n"
                f"Formula for {keyword}: {formula}\n"
                "Explain this formula clearly."
            )
        else:
            prompt = f"Query: '{query}'\nNo formula found for '{keyword}'."
    
    elif intent == "swap" and keyword:
        # CAPABILITIES METRIC: Query swap operation details
        operations = rag.query_protocol_operations("uniswap-v3")
        requirements = rag.get_operation_requirements("swap")
        outputs = rag.get_operation_outputs("swap")
        
        prompt = (
            f"Query: '{query}'\n"
            f"Protocol: Uniswap V3\n"
            f"Operation: swap\n"
            f"Required Parameters: {', '.join(requirements) if requirements else 'none'}\n"
            f"Expected Outputs: {', '.join(outputs) if outputs else 'none'}\n"
            "Explain how to execute this swap operation."
        )
    
    elif intent == "constraint" and keyword:
        # DOMAIN METRIC: Query price impact constraints
        constraints = rag.get_operation_constraints("swap")
        best_practices = rag.get_best_practices("swap")
        
        if constraints:
            parsed_constraints = [rag.parse_constraint(c) for c in constraints]
            prompt = (
                f"Query: '{query}'\n"
                f"Topic: {keyword}\n"
                f"Constraints: {json.dumps(parsed_constraints, indent=2)}\n"
                f"Best Practices: {', '.join(best_practices) if best_practices else 'none'}\n"
                "Explain these DeFi constraints and why they matter."
            )
        else:
            prompt = f"Query: '{query}'\nNo constraints found for '{keyword}'."
    
    if not prompt:
        prompt = f"Query: '{query}'\nNo specific DeFi info found. Offer general assistance."

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
    Calculate final evaluation score based on 3 metric scores (MVP version).
    
    Implements the axiom: "Confident but wrong is worse than low-confidence that is right"
    
    Args:
        metric_scores: Dict of {metric_name: {score, confidence, evidence, failures}}
        Expected keys: 'correctness', 'capabilities', 'domain'
        
    Returns:
        Final attestation object ready for signing
    """
    # MVP weights aligned with test plan
    weights = {
        "correctness": 0.50,    # Base chain facts, addresses, formulas
        "capabilities": 0.35,   # Swap execution on Uniswap V3
        "domain": 0.15          # Price impact awareness
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
        "evaluator": "truth-swarm-metta-mvp",
        "timestamp": None,  # Should be set by caller
        "final_score": round(final_score, 2),
        "overall_confidence": round(overall_confidence, 2),
        "grade": grade,
        "metrics": metric_scores,
        "effective_scores": {k: round(v, 2) for k, v in effective_scores.items()},
        "weights": weights,
        "attestation_version": "1.0.0-mvp"
    }