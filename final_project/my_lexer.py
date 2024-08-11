import re

# Define token patterns
token_patterns = [
    ('FN', r'fn'),                       # Matches function keyword
    ('LAMBDA', r'lambda'),               # Matches lambda keyword
    ('IF', r'if'),                       # Matches if keyword
    ('THEN', r'then'),                   # Matches then keyword
    ('ELSE', r'else'),                   # Matches else keyword
    ('REC', r'rec'),                     # Matches recursive function keyword
    ('INTEGER', r'\d+'),                 # Matches integers
    ('BOOLEAN', r'TRUE|FALSE'),          # Matches boolean literals
    ('ARITH_OP', r'[-+*/%]'),            # Matches arithmetic operators
    ('BOOL_OP', r'&&|\|\|'),             # Matches boolean operators
    ('COMP_OP', r'==|!=|>|<|>=|<='),     # Matches comparison operators
    ('NOT', r'!'),                       # Matches the NOT operator
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),     # Matches identifiers (including function names)
    ('LPAREN', r'\('),                   # Matches left parenthesis
    ('RPAREN', r'\)'),                   # Matches right parenthesis
    ('ASSIGN', r'='),                    # Matches assignment operator
    ('COLON', r':'),                     # Matches colon for lambda expressions
    ('COMMA', r','),                     # Matches comma in function definitions and calls
    ('COMMENT', r'#.*'),                 # Matches comments
    ('WHITESPACE', r'\s+'),              # Matches whitespace (will be ignored)
]

# Combine all patterns into a single regex
master_pattern = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_patterns)

# Compile the master pattern into a regex object
master_regex = re.compile(master_pattern)

def tokenize(code):
    tokens = []
    for match in master_regex.finditer(code):
        for name, pattern in token_patterns:
            value = match.group(name)
            if value:
                if name == 'INTEGER':
                    value = int(value)  # Convert integers from string to int
                elif name == 'BOOLEAN':
                    value = (value == 'TRUE')  # Convert boolean strings to True/False
                if name not in ['COMMENT', 'WHITESPACE']:  # Skip comments and whitespace
                    tokens.append((name, value))
                break
    return tokens
