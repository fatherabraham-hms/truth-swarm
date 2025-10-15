# defi-rag.py
import re
from hyperon import MeTTa, E, S, ValueAtom

(WIP)
class DefiRAG:
    """
    Retrieval-Augmented Generation class for DeFi knowledge graph queries.
    
    Provides methods to query the DeFi knowledge graph for:
    - Protocol capabilities
    - Operation requirements and constraints
    - Security risks and best practices
    - Asset classifications
    - FAQ responses
    """
    
    def __init__(self, metta_instance: MeTTa):
        self.metta = metta_instance
    
    # ========================================
    # CAPABILITY QUERIES
    # ========================================
    
    def query_protocol_operations(self, protocol):
        """
        Find all operations supported by a protocol.
        
        Used for CAPABILITY evaluation: verify if agent correctly claims
        what operations a protocol supports.
        
        Args:
            protocol: Protocol name (e.g., "uniswap-v3", "aave-v3")
            
        Returns:
            List of operation names supported by the protocol
        """
        protocol = protocol.strip('"')
        query_str = f'!(match &self (protocol {protocol} $operation) $operation)'
        results = self.metta.run(query_str)
        print(f"[DefiRAG] Query: {query_str}")
        print(f"[DefiRAG] Results: {results}")
        
        unique_operations = list(set(str(r[0]) for r in results if r and len(r) > 0)) if results else []
        return unique_operations
    
    def query_protocols_for_operation(self, operation):
        """
        Find all protocols that support a given operation.
        
        Used for routing and capability assessment.
        
        Args:
            operation: Operation name (e.g., "swap", "borrow")
            
        Returns:
            List of protocol names that support the operation
        """
        operation = operation.strip('"')
        query_str = f'!(match &self (protocol $protocol {operation}) $protocol)'
        results = self.metta.run(query_str)
        print(f"[DefiRAG] Query: {query_str}")
        print(f"[DefiRAG] Results: {results}")
        
        unique_protocols = list(set(str(r[0]) for r in results if r and len(r) > 0)) if results else []
        return unique_protocols
    
    # ========================================
    # FUNCTIONAL CORRECTNESS QUERIES
    # ========================================
    
    def get_operation_requirements(self, operation):
        """
        Find required parameters for an operation.
        
        Used for FUNCTIONAL CORRECTNESS evaluation: verify agent includes
        all required parameters when executing operations.
        
        Args:
            operation: Operation name (e.g., "swap", "borrow")
            
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
        Find expected outputs for an operation.
        
        Used for FUNCTIONAL CORRECTNESS: verify agent returns expected outputs.
        
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
    # DOMAIN CORRECTNESS QUERIES
    # ========================================
    
    def get_operation_constraints(self, operation):
        """
        Find financial/domain constraints for an operation.
        
        Used for DOMAIN CORRECTNESS evaluation: verify agent respects
        DeFi-specific rules (slippage limits, leverage ratios, etc.).
        
        Args:
            operation: Operation name
            
        Returns:
            List of constraint strings (e.g., "slippage_max:5.0")
        """
        operation = operation.strip('"')
        query_str = f'!(match &self (constraint {operation} $constraint) $constraint)'
        results = self.metta.run(query_str)
        print(f"[DefiRAG] Query: {query_str}")
        print(f"[DefiRAG] Results: {results}")
        
        return [r[0].get_object().value for r in results if r and len(r) > 0] if results else []
    
    def parse_constraint(self, constraint_string):
        """
        Parse a constraint string into key-value pairs.
        
        Args:
            constraint_string: String like "slippage_max:5.0"
            
        Returns:
            Tuple of (constraint_type, value)
        """
        if ':' in constraint_string:
            key, value = constraint_string.split(':', 1)
            try:
                # Try to convert to float if possible
                value = float(value)
            except ValueError:
                pass
            return (key, value)
        return (constraint_string, None)
    
    def get_constraint_value(self, operation, constraint_type):
        """
        Get specific constraint value for an operation.
        
        Args:
            operation: Operation name
            constraint_type: Constraint key (e.g., "slippage_max")
            
        Returns:
            Constraint value or None
        """
        constraints = self.get_operation_constraints(operation)
        for constraint_str in constraints:
            key, value = self.parse_constraint(constraint_str)
            if key == constraint_type:
                return value
        return None
    
    # ========================================
    # SECURITY & SAFETY QUERIES
    # ========================================
    
    def get_operation_risks(self, operation):
        """
        Find security risks associated with an operation.
        
        Used for SECURITY evaluation: verify agent is aware of and
        mitigates known risks.
        
        Args:
            operation: Operation name
            
        Returns:
            List of risk strings (e.g., "mev:frontrun,sandwich")
        """
        operation = operation.strip('"')
        query_str = f'!(match &self (risk {operation} $risk) $risk)'
        results = self.metta.run(query_str)
        print(f"[DefiRAG] Query: {query_str}")
        print(f"[DefiRAG] Results: {results}")
        
        return [r[0].get_object().value for r in results if r and len(r) > 0] if results else []
    
    def get_best_practices(self, operation):
        """
        Find security best practices for an operation.
        
        Used for SECURITY evaluation: verify agent follows best practices.
        
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
    
    # ========================================
    # DOMAIN KNOWLEDGE QUERIES
    # ========================================
    
    def query_asset_type(self, asset):
        """
        Find the classification of an asset (stable, volatile, lst).
        
        Used for applying appropriate constraints based on asset risk profile.
        
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
    
    def query_protocol_tvl(self, protocol):
        """
        Find the TVL (Total Value Locked) for a protocol.
        
        Used for OPERATIONAL evaluation: assess protocol reliability/size.
        
        Args:
            protocol: Protocol name
            
        Returns:
            TVL value as string or None
        """
        protocol = protocol.strip('"')
        query_str = f'!(match &self (tvl {protocol} $tvl) $tvl)'
        results = self.metta.run(query_str)
        print(f"[DefiRAG] Query: {query_str}")
        print(f"[DefiRAG] Results: {results}")
        
        return results[0][0].get_object().value if results and results[0] else None
    
    # ========================================
    # FAQ QUERIES
    # ========================================
    
    def query_faq(self, question):
        """
        Retrieve FAQ answers.
        
        Used for EXPLAINABILITY: provide educational context.
        
        Args:
            question: Question string
            
        Returns:
            Answer string or None
        """
        query_str = f'!(match &self (faq "{question}" $answer) $answer)'
        results = self.metta.run(query_str)
        print(f"[DefiRAG] Query: {query_str}")
        print(f"[DefiRAG] Results: {results}")
        
        return results[0][0].get_object().value if results and results[0] else None
    
    # ========================================
    # KNOWLEDGE ADDITION
    # ========================================
    
    def add_knowledge(self, relation_type, subject, object_value):
        """
        Add new knowledge dynamically to the graph.
        
        Args:
            relation_type: Type of relation (e.g., "protocol", "constraint", "risk")
            subject: Subject of the relation
            object_value: Object value (converted to ValueAtom if string)
            
        Returns:
            Confirmation string
        """
        if isinstance(object_value, str):
            object_value = ValueAtom(object_value)
        self.metta.space().add_atom(E(S(relation_type), S(subject), object_value))
        return f"Added {relation_type}: {subject} → {object_value}"
    
    # ========================================
    # EVALUATION HELPER METHODS
    # ========================================
    
    def validate_operation_params(self, operation, provided_params):
        """
        Validate that all required parameters are provided.
        
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
                "message": "No requirements found for this operation"
            }
        
        # Parse required params (comma-separated string)
        required_params = required[0].split(',') if required else []
        
        # Convert provided_params to set of names
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
            "message": "All required parameters provided" if not missing else f"Missing: {', '.join(missing)}"
        }
    
    def check_constraint_violation(self, operation, param_name, param_value):
        """
        Check if a parameter value violates domain constraints.
        
        Args:
            operation: Operation name
            param_name: Parameter name (e.g., "slippage")
            param_value: Parameter value to check
            
        Returns:
            Dict with violation results
        """
        constraints = self.get_operation_constraints(operation)
        violations = []
        warnings = []
        
        for constraint_str in constraints:
            key, threshold = self.parse_constraint(constraint_str)
            
            # Check if this constraint applies to the parameter
            if param_name in key.lower():
                try:
                    value_float = float(param_value)
                    threshold_float = float(threshold)
                    
                    if 'max' in key and value_float > threshold_float:
                        violations.append({
                            "constraint": key,
                            "threshold": threshold_float,
                            "actual": value_float,
                            "message": f"{param_name} exceeds maximum of {threshold_float} (got {value_float})"
                        })
                    elif 'min' in key and value_float < threshold_float:
                        violations.append({
                            "constraint": key,
                            "threshold": threshold_float,
                            "actual": value_float,
                            "message": f"{param_name} below minimum of {threshold_float} (got {value_float})"
                        })
                    elif 'warn' in key and value_float > threshold_float:
                        warnings.append({
                            "constraint": key,
                            "threshold": threshold_float,
                            "actual": value_float,
                            "message": f"{param_name} above warning threshold of {threshold_float} (got {value_float})"
                        })
                except (ValueError, TypeError):
                    pass
        
        return {
            "has_violations": len(violations) > 0,
            "violations": violations,
            "warnings": warnings,
            "message": "No violations" if not violations else f"Found {len(violations)} violation(s)"
        }
    
    def get_comprehensive_operation_info(self, operation):
        """
        Get all available information about an operation.
        
        Useful for generating evaluation reports.
        
        Args:
            operation: Operation name
            
        Returns:
            Dict with all operation information
        """
        return {
            "operation": operation,
            "protocols": self.query_protocols_for_operation(operation),
            "requirements": self.get_operation_requirements(operation),
            "outputs": self.get_operation_outputs(operation),
            "constraints": self.get_operation_constraints(operation),
            "risks": self.get_operation_risks(operation),
            "best_practices": self.get_best_practices(operation)
        }

