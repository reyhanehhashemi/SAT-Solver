from cnf import CNF
import logging

class CSP:
    def __init__(self, cnf: CNF, use_mcv=True, use_mrv=True, use_lcv=True):
        """
        Initializes a Constraint Satisfaction Problem (CSP) solver.

        Args:
            cnf (CNF): The Conjunctive Normal Form representation of the problem.
            use_mcv (bool): Whether to use Most Constraining Variable (MCV) or not. Defaults to True.
            use_mrv (bool): Whether to use Minimum Remaining Value (MRV) or not. Defaults to True.
            use_lcv (bool): Whether to use Least Constraining Value (LCV) or not. Defaults to True.
        """
        self.cnf = cnf
        self.use_mcv = use_mcv
        self.use_mrv = use_mrv
        self.use_lcv = use_lcv
        self.degree_variables = {}
        self.variables = {}  
        self.assigned_variables = {}  
        self.constraints = []  
        self.var_constraints = {} 
        
       
        if self.use_mcv and self.use_mrv:
            raise ValueError("MRV and MCV cannot be used together. Please select one heuristic.")

        
        if cnf and cnf.variables:
            real_vars = {lit.strip('~') for lit in cnf.variables}
            for var in real_vars:
                self.variables[var] = [False, True]  

    def add_variable(self, variable, domain):
        """
        Adds a new variable with its given domain to the CSP solver.

        Args:
            variable (str): The name of the variable.
            domain ([bool]): The domain of the variable (in this case, [False, True]).
        """
        self.variables[variable] = domain

    def add_constraint(self, constraint_function, variables):
        """
        Adds a new constraint to the CSP solver.

        Args:
            constraint_function (function): A function that takes an assignment (dict) and returns True
                                              if the constraint is satisfied, False otherwise.
            variables ([str]): The list of variables involved in the constraint.
        """
        constraint = (constraint_function, variables)
        self.constraints.append(constraint)
        for var in variables:
            if var not in self.var_constraints:
                self.var_constraints[var] = []
            self.var_constraints[var].append(constraint)

    def assign(self, variable, value):
        """
        Assigns a specific value to a variable.

        Args:
            variable (str): The name of the variable.
            value (bool): The assigned value for the variable.
        """
        self.assigned_variables[variable] = value

    def unassign(self, variable):
        """
        Unassigns a previously assigned value from a variable.

        Args:
            variable (str): The name of the variable.
        """
        if variable in self.assigned_variables:
            del self.assigned_variables[variable]

    def is_constraint_satisfied(self, constraint):
        """
        Checks if a specific constraint is satisfied given the current assignment of variables.

        Args:
            constraint: A tuple containing the constraint function and the list of involved variables.

        Returns:
            bool: True if the constraint is satisfied, False otherwise.
        """
        func, vars_in_constraint = constraint
        if all(var in self.assigned_variables for var in vars_in_constraint):
            return func(self.assigned_variables)
        return True

    def is_consistent(self, variable, value):
        """
        Checks if assigning a specific value to a variable would violate any constraints.

        Args:
            variable (str): The name of the variable.
            value (bool): The assigned value for the variable.

        Returns:
            bool: True if the assignment does not violate any constraints, False otherwise.
        """
        temp_assignment = self.assigned_variables.copy()
        temp_assignment[variable] = value
        
       
        fully_assigned = list(filter(
            lambda clause: all(lit.strip('~') in temp_assignment for lit in clause),
            self.cnf.hard_clauses
        ))
        unsatisfied = list(filter(
            lambda clause: not self.cnf.evaluate_clause(clause, temp_assignment),
            fully_assigned
        ))
        if unsatisfied:
            return False

        
        for constraint in self.constraints:
            if not self.is_constraint_satisfied(constraint):
                return False

        return True

    def is_complete(self):
        """
        Checks if all variables have been assigned a value.

        Returns:
            bool: True if the assignment is complete, False otherwise.
        """
        return len(self.assigned_variables) == len(self.variables)

    def minimum_remaining_value(self):
        """
        Selects the unassigned variable with the fewest legal values (MRV heuristic).

        Returns:
            str: The name of the selected variable.
        """
        unassigned = [var for var in self.variables if var not in self.assigned_variables]
        min_legal = 3  
        selected = None
        for var in unassigned:
            legal = 0
            for value in [True, False]:
                if self.is_consistent(var, value):
                    legal += 1
            if legal < min_legal:
                min_legal = legal
                selected = var
        return selected

    def most_constraining_variable(self, unassigned_variables):
        """
        Returns the variable that would violate the most constraints when assigned a value.

        Args:
            unassigned_variables ([str]): The list of unassigned variables.

        Returns:
            str: The name of the most constraining variable.
        """
        max_degree = -1
        selected = None
        for var in unassigned_variables:
            degree = 0
            for clause in self.cnf.hard_clauses:
                if self.cnf.evaluate_clause(clause, self.assigned_variables):
                    continue
                if var in clause or ('~' + var) in clause:
                    degree += 1
            if degree > max_degree:
                max_degree = degree
                selected = var
        return selected

    def least_constraining_value(self, var):
        """
        Returns the value that would violate the fewest constraints when assigned to a variable.

        Args:
            var (str): The name of the variable.

        Returns:
            bool: The least constraining value for the variable.
        """
        scores = {}
        for value in [True, False]:
            temp_assign = self.assigned_variables.copy()
            temp_assign[var] = value
            violation = 0
            for clause in self.cnf.hard_clauses:
                fully_assigned = all(lit.strip('~') in temp_assign for lit in clause)
                if fully_assigned and not self.cnf.evaluate_clause(clause, temp_assign):
                    violation += 1
            scores[value] = violation
        return True if scores[True] <= scores[False] else False

    def select_unassigned_variable(self):
        """
        Selects an unassigned variable to assign a value to next.

        Returns:
            str: The name of the selected variable.
        """
        unassigned = [var for var in self.variables if var not in self.assigned_variables]
        
      
        if self.use_mrv:
            var = self.minimum_remaining_value()
            if var is not None:
                return var
        
      
        if self.use_mcv and not self.use_mrv:
            var = self.most_constraining_variable(unassigned)
            if var is not None:
                return var
        
        return unassigned[0] if unassigned else None

    def optimistic_bound(self, assignments):
        """
        Computes an optimistic bound for the current partial assignment.
        
        Returns:
            int: optimistic bound.
        """
        bound = 0
        for clause in self.cnf.soft_clauses:
            literals = clause[:-1]
            weight = int(clause[-1])
            if all(lit.strip('~') in assignments for lit in literals):
                if self.cnf.evaluate_clause(literals, assignments):
                    bound += weight
            else:
                bound += weight
        return bound

    def solve(self):
        """
        Solves the CSP problem using backtracking search with added filtering:
          - Forward Checking
          - Branch and Bound
        
        Returns:
            tuple: (solution, best_weight)
        """
        self.best_solution = None
        self.best_weight = -1
        self.assigned_variables = {}

        def backtrack():
           
            fully_assigned = list(filter(
                lambda clause: all(lit.strip('~') in self.assigned_variables for lit in clause),
                self.cnf.hard_clauses
            ))
            unsatisfied = list(filter(
                lambda clause: not self.cnf.evaluate_clause(clause, self.assigned_variables),
                fully_assigned
            ))
            if unsatisfied:
                return

            current_bound = self.optimistic_bound(self.assigned_variables)
            if current_bound <= self.best_weight:
                return

            if self.is_complete():
                current_weight = self.cnf.calculate_weight(self.assigned_variables)
                if current_weight > self.best_weight:
                    self.best_weight = current_weight
                    self.best_solution = self.assigned_variables.copy()
                return

            var = self.select_unassigned_variable()
            if var is None:
                return

            if self.use_lcv:
                preferred_value = self.least_constraining_value(var)
                values = [preferred_value, not preferred_value]
            else:
                values = [True, False]

            for value in values:
                if self.is_consistent(var, value):
                    self.assign(var, value)
                    backtrack()
                    self.unassign(var)

        backtrack()
        return self.best_solution, self.best_weight
