import re
import operator
import pyodbc

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left  # Left node (for operators)
        self.right = right  # Right node (for operators)
        self.value = value  # Value for operand nodes (e.g., comparisons like age > 30)

    def __repr__(self):
        return f"Node(type={self.type}, left={self.left}, right={self.right}, value={self.value})"


# SQL Server connection using Windows Authentication
def get_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=LAPTOP-TD2RCIUT\\SQLEXPRESS;'  # Your server name
        'DATABASE=Rule_engine;'  # Your database name
        'Trusted_Connection=yes;'  # Use Windows Authentication
    )
    return conn

# Insert rule into the database
def insert_rule_to_db(rule_string):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Rules (RuleString) VALUES (?)", (rule_string,))
    conn.commit()
    conn.close()

# Fetch rules from the database
def fetch_rules_from_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT RuleID, RuleString FROM Rules")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Operators for parsing and evaluating conditions
ops = {
    'AND': operator.and_,
    'OR': operator.or_,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
}

# Parse conditions into AST nodes
def parse_condition(condition_str):
    for op_symbol in ops:
        if op_symbol in condition_str:
            # Split based on the first occurrence of the operator
            left, right = re.split(rf"\s*{re.escape(op_symbol)}\s*", condition_str, maxsplit=1)
            return Node("operand", value=(left.strip(), op_symbol, right.strip()))
    raise ValueError(f"Unknown condition: {condition_str}")

# Create AST from rule string
def create_rule(rule_string):
    """Convert a rule string to an AST."""
    stack = []
    
    # Use regex to tokenize the rule string (capture everything inside conditions)
    tokens = re.findall(r'\(|\)|AND|OR|[a-zA-Z_]+\s*(==|!=|>|<|>=|<=)\s*\'?[a-zA-Z0-9_ ]+\'?', rule_string)

    for token in tokens:
        if token == '(':
            stack.append(token)
        elif token == ')':
            right = stack.pop()
            operator_node = stack.pop()
            left = stack.pop()
            stack.pop()  # pop the '('
            operator_node.left = left
            operator_node.right = right
            stack.append(operator_node)
        elif token in ('AND', 'OR'):
            stack.append(Node("operator", value=token))
        else:
            # For conditions like 'age > 30' or 'department == "Sales"'
            stack.append(parse_condition(token))

    return stack.pop()

# Combine multiple rule ASTs
def combine_rules(rule_strings):
    combined_node = None
    for rule_string in rule_strings:
        new_rule_ast = create_rule(rule_string)
        if combined_node is None:
            combined_node = new_rule_ast
        else:
            combined_node = Node("operator", left=combined_node, right=new_rule_ast, value='AND')
    return combined_node

# Evaluate AST nodes
def evaluate_node(node, data):
    if node.type == 'operand':
        left, op_symbol, right = node.value
        left_value = data.get(left)
        if left_value is None:
            raise ValueError(f"Missing data for '{left}'")
        return ops[op_symbol](left_value, float(right) if right.replace('.', '', 1).isdigit() else right)
    elif node.type == 'operator':
        left_result = evaluate_node(node.left, data)
        right_result = evaluate_node(node.right, data)
        return ops[node.value](left_result, right_result)

# Evaluate the entire AST against the provided data
def evaluate_rule(ast, data):
    return evaluate_node(ast, data)

# Main function to test the rule engine
def test():
    # Fetch rules from the database
    rules = fetch_rules_from_db()
    for rule_id, rule_string in rules:
        print(f"Fetched RuleID: {rule_id}, Rule: {rule_string}")
    
    # Sample rule strings
    rule1 = "((age > 30 AND department == 'Sales') OR (age < 25 AND department == 'Marketing')) AND (salary > 50000 OR experience > 5)"
    rule2 = "((age > 30 AND department == 'Marketing')) AND (salary > 20000 OR experience > 5)"
    
    # Create AST from rule1
    ast1 = create_rule(rule1)
    print("AST for rule1:", ast1)

    # Combine rule1 and rule2 into a single AST
    combined_ast = combine_rules([rule1, rule2])
    print("Combined AST:", combined_ast)

    # Sample data
    sample_data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}

    # Evaluate rule1
    result = evaluate_rule(ast1, sample_data)
    print("Evaluation result for rule1:", result)

    # Evaluate combined rules
    combined_result = evaluate_rule(combined_ast, sample_data)
    print("Evaluation result for combined rules:", combined_result)


if __name__ == "__main__":
    test()
