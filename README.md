# SAT Solver using CSP 

## 📋 Project Overview

This project implements a **SAT Solver** using **Constraint Satisfaction Problem (CSP)** techniques with a graphical user interface. The solver handles Boolean satisfiability problems in Conjunctive Normal Form (CNF) and supports both hard constraints (must be satisfied) and soft constraints (weighted, optional satisfaction).

## 🏗️ Project Structure

### Core Components

- **`cnf.py`** - CNF formula representation and evaluation
  - `CNF` class for managing variables, hard clauses, and soft clauses
  - Methods for clause evaluation and weight calculation

- **`csp.py`** - CSP solver implementation
  - `CSP` class with backtracking search
  - Support for MRV, MCV, and LCV heuristics
  - Branch and Bound optimization

- **`ui.py`** - PyQt6-based graphical interface
  - File selection for test cases
  - Heuristic configuration
  - Results display

- **`main.py`** - Application entry point

### Test Files

- **`t1.txt`, `t2.txt`, `t3.txt`, `t4.txt`** - Sample test cases
- **`test_case_generator.py`** - Utility for generating custom test cases

## 🚀 Features

### SAT Solving
- **CNF Formula Processing** - Parses and evaluates Boolean formulas
- **Hard Constraints** - Clauses that must be satisfied
- **Soft Constraints** - Weighted clauses for optimization (MaxSAT)

### CSP Heuristics
- **MRV (Minimum Remaining Values)** - Selects variable with fewest legal values
- **MCV (Most Constraining Variable)** - Selects variable involved in most constraints
- **LCV (Least Constraining Value)** - Chooses value that rules out fewest values

### Optimization
- **Backtracking Search** - Systematic exploration of solution space
- **Forward Checking** - Constraint propagation
- **Branch and Bound** - Prunes unpromising branches using optimistic bounds

## 🛠️ Installation & Usage

### Prerequisites
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
python main.py
```

### Generating Test Cases
```bash
python test_case_generator.py <num_vars> <num_clauses> <num_soft_clauses> <max_weight> <test_file>
```

## 📊 Usage Instructions

1. **Launch the application** - Run `main.py` to start the GUI
2. **Select test file** - Choose a CNF file using the file dialog
3. **Configure heuristics** - Select MRV, MCV, and/or LCV (note: MRV and MCV are mutually exclusive)
4. **Solve** - Click "Solve" to find the optimal assignment
5. **View results** - See maximum weight, execution time, and variable assignments

## 🧩 Algorithm Details

### Backtracking Search
- Recursively assigns values to variables
- Checks consistency at each step
- Backtracks when constraints are violated

### Heuristic Improvements
- **MRV**: Reduces branching factor by choosing most constrained variables first
- **MCV**: Maximizes constraint propagation by choosing highly connected variables
- **LCV**: Maintains flexibility by choosing values that leave maximum options

### Branch and Bound
- Computes optimistic bounds for partial assignments
- Prunes branches that cannot improve current best solution
- Efficiently explores solution space for weighted MaxSAT problems

## 📈 Performance Considerations

- **Time Complexity**: Exponential in worst case, but heuristics significantly improve practical performance
- **Space Complexity**: Linear in number of variables for storage, plus recursion depth
- **Optimization**: Branch and Bound reduces search space for weighted problems

## 🎯 Key Results

The solver successfully:
- Finds satisfying assignments for satisfiable formulas
- Maximizes weights for soft constraints in unsatisfiable cases
- Provides execution time metrics for performance comparison
- Supports various heuristic combinations for different problem types

## 📝 File Format

Test files follow this structure:
```
<num_variables> <num_hard_clauses> <num_soft_clauses>
<hard_clause_1>
<hard_clause_2>
...
SOFT_CLAUSE <literals> <weight>
SOFT_CLAUSE <literals> <weight>
...
```

## 🔧 Customization

- Modify heuristic preferences in CSP constructor
- Extend CNF class for additional formula types
- Add new constraint types in CSP constraints system

## 📄 License

This project was developed as part of an Artificial Intelligence course at Amirkabir University of Technology.

---

*For detailed implementation details and algorithm analysis, refer to the project documentation and source code comments.*
