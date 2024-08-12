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
        # Function definition
        '''
        Defun {name: factorial, arguments: (n,y,)}
        (n == 0) || (n * factorial(y - 1,0,))
        ''',
        # Lambda expression
        '''
        (Lambd x.(Lambd y.(x + y)))(3,5)
        ''',
        # Function application
        '''
        factorial(5)
        ''',
        # Boolean operations
        '''
        (x > 0) && (y < 10)
        ''',
        # Arithmetic operations
        '''
        (3 + 4) * (2 - 1)
        '''
    ]

    for i, code in enumerate(test_cases, start=1):
        print(f"Test Case {i}:\n")
        run_test_case(code, bnf_file_path)
        print("\n" + "=" * 40 + "\n")

if __name__ == "__main__":
    main()