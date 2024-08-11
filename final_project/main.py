from my_lexer import tokenize
from my_parser import Parser

def main():
    # Sample input code
    code = '''
    fn add(x, y) = x + y
    '''

    # Path to the BNF file
    bnf_file_path = 'BNF.txt'

    # Tokenize the input
    tokens = tokenize(code)
    print("Tokens:")
    for token in tokens:
        print(token)

    # Parse the tokens into an AST
    parser = Parser(tokens, bnf_file_path)
    ast = parser.parse()

    # Print the AST
    print("\nAbstract Syntax Tree (AST):")
    for node in ast:
        print(node)

if __name__ == "__main__":
    main()
