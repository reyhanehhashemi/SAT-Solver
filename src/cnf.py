class CNF:
    def __init__(self, variables, hard_clauses, soft_clauses):
        """
        Initializes a Conjunctive Normal Form (CNF) object.

        Args:
            variables (list): List of variable names.
            hard_clauses (list): List of hard clauses. Each clause is a list of literals.
            soft_clauses (list): List of soft clauses, where each soft clause is a list (or tuple)
                                 that ends with a weight (int or float).
        """
        self.variables = variables
        self.hard_clauses = hard_clauses
        self.soft_clauses = soft_clauses

    def evaluate_clause(self, clause, assignments):
        """
        Checks if a single clause is satisfied given the assignments.
        A clause is satisfied if at least one of its literals evaluates to True.

        Args:
            clause (list): A list of literals.
            assignments (dict): A dictionary mapping variable names to booleans.

        Returns:
            bool: True if the clause is satisfied, False otherwise.
        """
        for literal in clause:
            
            if literal.startswith('-') or literal.startswith('~') or literal.startswith('¬'):
                if self.evaluate_negation(literal, assignments):
                    return True
            else:
                
                if assignments.get(literal, False):
                    return True
        return False

    def evaluate_negation(self, literal, assignments):
        """
        Checks if a negated literal is satisfied.
        A literal (e.g., '-x1') is satisfied if the corresponding variable is False.

        Args:
            literal (str): A literal that is expected to be negated.
            assignments (dict): A dictionary mapping variable names to booleans.

        Returns:
            bool: True if the negated literal is satisfied, False otherwise.
        """
        
        var = literal.lstrip('-~¬')
        
        return not assignments.get(var, False)

    def calculate_weight(self, assignments):
        """
        Calculates the total weight of satisfied soft clauses based on the given assignments.

        Args:
            assignments (dict): Dictionary where keys are variable names and values are booleans.

        Returns:
            int or float: The sum of weights for all soft clauses that are satisfied.
        """
        total_weight = 0
        for soft_clause in self.soft_clauses:
            
            weight = int(soft_clause[-1])
            clause = soft_clause[:-1]
            if self.evaluate_clause(clause, assignments):
                total_weight += weight
        return total_weight
