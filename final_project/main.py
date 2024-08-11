from my_lexer import tokenize
from my_parser import Parser

def run_test_case(code, bnf_file_path):
    print("Running test case...\n")

    # Tokenize the input
    tokens = tokenize(code)
    print("Tokens:")
    for token in tokens:
        print(token)

    # Parse the tokens into an AST
    parser = Parser(tokens, bnf_file_path)

    try:
        ast = parser.parse()
        print("\nAbstract Syntax Tree (AST):")
        for node in ast:
            print(node)
    except Exception as e:
        print(f"An error occurred during parsing: {e}")

def main():
    # Path to the BNF file
    bnf_file_path = 'BNF.txt'

    # Define various test cases
    test_cases = [
        # Simple function definition
        '''
        fn add(x, y) = x + y
        ''',
        # Lambda expression
        '''
        lambda x : x > 0 && TRUE
        ''',
        # Conditional expression
        '''
        if x < 10 then lambda y: 0 else lambda z: 1
        ''',
        # Recursion example
        '''
        rec factorial(n) = if n == 0 then lambda x: 1 else lambda m: n * factorial(m - 1)
        '''
    ]

    for i, code in enumerate(test_cases, start=1):
        print(f"Test Case {i}:\n")
        run_test_case(code, bnf_file_path)
        print("\n" + "=" * 40 + "\n")

if __name__ == "__main__":
    main()
