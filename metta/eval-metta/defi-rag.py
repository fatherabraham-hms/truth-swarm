# defi-rag.py
import re
from hyperon import MeTTa, E, S, ValueAtom

(WIP)
class DefiRAG:
    """
    Minimal RAG for DeFi agent evaluation (MVP/POC version).
    
    Supports 3 evaluation metrics:
    1. Correctness: Query chain info, addresses, formulas
    2. Capabilities: Query protocol operations and requirements
    3. Domain Knowledge: Query price impact constraints
    """
    
    def __init__(self, metta_instance: MeTTa):
        self.metta = metta_instance
    
    # ========================================
    # CORRECTNESS METRIC QUERIES
    # ========================================
    
    def query_chain_info(self, chain_name):
        """
        Get chain information (e.g., chainId for Base).
        
        Args:
            chain_name: Chain name (e.g., "base")
            
        Returns:
            Chain info string (e.g., "chainId:8453") or None
        """
        chain_name = chain_name.strip('"')
        query_str = f'!(match &self (chain {chain_name} $info) $info)'
        results = self.metta.run(query_str)
        print(f"[DefiRAG] Query: {query_str}")
        print(f"[DefiRAG] Results: {results}")
        
        return results[0][0].get_object().value if results and results[0] else None
    
    def query_token_address(self, token_chain):
        """
        Get canonical token address on specific chain.
        
        Args:
            token_chain: Token-chain combo (e.g., "USDC-base")
            
        Returns:
            Token address or None
        """
        token_chain = token_chain.strip('"')
        query_str = f'!(match &self (token-address {token_chain} $address) $address)'
        results = self.metta.run(query_str)
        print(f"[DefiRAG] Query: {query_str}")
        print(f"[DefiRAG] Results: {results}")
        
        return results[0][0].get_object().value if results and results[0] else None
    
    def query_protocol_address(self, protocol_chain):
        """
        Get protocol contract address on specific chain.
        
        Args:
            protocol_chain: Protocol-chain combo (e.g., "uniswap-v3-base")
            
        Returns:
            Protocol address or None
        """
        protocol_chain = protocol_chain.strip('"')
        query_str = f'!(match &self (protocol-address {protocol_chain} $address) $address)'
        results = self.metta.run(query_str)
        print(f"[DefiRAG] Query: {query_str}")
        print(f"[DefiRAG] Results: {results}")
        
        return results[0][0].get_object().value if results and results[0] else None
    
    def query_formula(self, formula_name):
        """
        Get formula/calculation (e.g., slippage calculation).
        
        Args:
            formula_name: Formula name (e.g., "slippage")
            
        Returns:
            Formula string or None
        """
        formula_name = formula_name.strip('"')
        query_str = f'!(match &self (formula {formula_name} $formula) $formula)'
        results = self.metta.run(query_str)
        print(f"[DefiRAG] Query: {query_str}")
        print(f"[DefiRAG] Results: {results}")
        
        return results[0][0].get_object().value if results and results[0] else None
    
    # ========================================
    # CAPABILITIES METRIC QUERIES
    # ========================================
    
    def query_protocol_operations(self, protocol):
        """
        Find operations supported by a protocol.
        
        Args:
            protocol: Protocol name (e.g., "uniswap-v3")
            
        Returns:
            List of operation names
        """
        protocol = protocol.strip('"')
        query_str = f'!(match &self (protocol {protocol} $operation) $operation)'
        results = self.metta.run(query_str)
        print(f"[DefiRAG] Query: {query_str}")
        print(f"[DefiRAG] Results: {results}")
        
        unique_operations = list(set(str(r[0]) for r in results if r and len(r) > 0)) if results else []
        return unique_operations
    
    def get_operation_requirements(self, operation):
        """
        Get required parameters for an operation.
        
        Args:
            operation: Operation name (e.g., "swap")
            
        Returns:
            List of required parameter strings
        """
        operation = operation.strip('"')
        query_str = f'!(match &self (requires {operation} $params) $params)'
        results = self.metta.run(query_str)
        print(f"[DefiRAG] Query: {query_str}")
        print(f"[DefiRAG] Results: {results}")
        
        return [r[0].get_object().value for r in results if r and len(r) > 0] if results else []
    
    def get_operation_outputs(self, operation):
        """
        Get expected outputs for an operation.
        
        Args:
            operation: Operation name
            
        Returns:
            List of expected output strings
        """
        operation = operation.strip('"')
        query_str = f'!(match &self (output {operation} $outputs) $outputs)'
        results = self.metta.run(query_str)
        print(f"[DefiRAG] Query: {query_str}")
        print(f"[DefiRAG] Results: {results}")
        
        return [r[0].get_object().value for r in results if r and len(r) > 0] if results else []
    
    # ========================================
    # DOMAIN KNOWLEDGE QUERIES
    # ========================================
    
    def get_operation_constraints(self, operation):
        """
        Get domain constraints for an operation (e.g., price impact limits).
        
        Args:
            operation: Operation name
            
        Returns:
            List of constraint strings (e.g., "price_impact_max:10.0")
        """
        operation = operation.strip('"')
        query_str = f'!(match &self (constraint {operation} $constraint) $constraint)'
        results = self.metta.run(query_str)
        print(f"[DefiRAG] Query: {query_str}")
        print(f"[DefiRAG] Results: {results}")
        
        return [r[0].get_object().value for r in results if r and len(r) > 0] if results else []
    
    def get_best_practices(self, operation):
        """
        Get best practices for an operation.
        
        Args:
            operation: Operation name
            
        Returns:
            List of best practice strings
        """
        operation = operation.strip('"')
        query_str = f'!(match &self (best-practice {operation} $practice) $practice)'
        results = self.metta.run(query_str)
        print(f"[DefiRAG] Query: {query_str}")
        print(f"[DefiRAG] Results: {results}")
        
        return [r[0].get_object().value for r in results if r and len(r) > 0] if results else []
    
    def parse_constraint(self, constraint_string):
        """
        Parse a constraint string into key-value pairs.
        
        Args:
            constraint_string: String like "price_impact_max:10.0"
            
        Returns:
            Tuple of (constraint_type, value)
        """
        if ':' in constraint_string:
            key, value = constraint_string.split(':', 1)
            try:
                value = float(value)
            except ValueError:
                pass
            return (key, value)
        return (constraint_string, None)
    
    # ========================================
    # SUPPORTING QUERIES
    # ========================================
    
    def query_asset_type(self, asset):
        """
        Get asset classification (stable, volatile).
        
        Args:
            asset: Asset symbol (e.g., "USDC", "ETH")
            
        Returns:
            Asset type string or None
        """
        asset = asset.strip('"')
        query_str = f'!(match &self (asset-type {asset} $type) $type)'
        results = self.metta.run(query_str)
        print(f"[DefiRAG] Query: {query_str}")
        print(f"[DefiRAG] Results: {results}")
        
        return str(results[0][0]) if results and results[0] else None
    
    # ========================================
    # EVALUATION HELPERS
    # ========================================
    
    def validate_operation_params(self, operation, provided_params):
        """
        Validate required parameters are provided.
        
        Args:
            operation: Operation name
            provided_params: List or dict of provided parameter names
            
        Returns:
            Dict with validation results
        """
        required = self.get_operation_requirements(operation)
        
        if not required:
            return {
                "valid": True,
                "missing": [],
                "message": "No requirements found"
            }
        
        required_params = required[0].split(',') if required else []
        
        if isinstance(provided_params, dict):
            provided_set = set(provided_params.keys())
        else:
            provided_set = set(provided_params)
        
        required_set = set(p.strip() for p in required_params)
        missing = required_set - provided_set
        
        return {
            "valid": len(missing) == 0,
            "missing": list(missing),
            "required": list(required_set),
            "provided": list(provided_set),
            "message": "Valid" if not missing else f"Missing: {', '.join(missing)}"
        }
    
    def check_price_impact_violation(self, price_impact_percent):
        """
        Check if price impact exceeds domain constraints (>10%).
        
        Args:
            price_impact_percent: Price impact as percentage
            
        Returns:
            Dict with violation info
        """
        constraints = self.get_operation_constraints("swap")
        violations = []
        warnings = []
        
        for constraint_str in constraints:
            key, threshold = self.parse_constraint(constraint_str)
            
            if 'price_impact' in key:
                try:
                    impact_float = float(price_impact_percent)
                    threshold_float = float(threshold)
                    
                    if 'max' in key and impact_float > threshold_float:
                        violations.append({
                            "constraint": key,
                            "threshold": threshold_float,
                            "actual": impact_float,
                            "message": f"Price impact {impact_float}% exceeds max {threshold_float}%"
                        })
                    elif 'warn' in key and impact_float > threshold_float:
                        warnings.append({
                            "constraint": key,
                            "threshold": threshold_float,
                            "actual": impact_float,
                            "message": f"Price impact {impact_float}% triggers warning at {threshold_float}%"
                        })
                except (ValueError, TypeError):
                    pass
        
        return {
            "has_violations": len(violations) > 0,
            "violations": violations,
            "warnings": warnings,
            "message": "OK" if not violations else f"Found {len(violations)} violation(s)"
        }

