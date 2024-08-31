from my_interpreter2 import Interpreter
from my_lexer import tokenize
from my_parser import Parser
import sys

def main():
    interpreter = Interpreter()  # Create a single Interpreter instance

    if len(sys.argv) > 1:
        # Run the interpreter with a program file
        file_path = sys.argv[1]
        with open(file_path, 'r') as file:
            code = file.read()
        try:
            tokens = tokenize(code)
            parser = Parser(tokens, 'BNF.txt')
            ast = parser.parse()
            interpreter.interpret(ast)  # Use the existing interpreter instance
        except Exception as e:
            print(f"Error: {e}")
    else:
        # Run the interpreter in interactive mode
        print("Interactive mode. Type 'exit' or 'quit' to exit.")
        while True:
            try:
                code = input(">>> ").strip()
                if code.lower() in ['exit', 'quit']:
                    break
                tokens = tokenize(code)
                parser = Parser(tokens, 'BNF.txt')
                ast = parser.parse()
                print(ast)
                result = interpreter.interpret(ast)  # Use the existing interpreter instance
                print(result)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()


#Defun { name: factorial, arguments: (n,) } (n == 0) || (n * factorial(n - 1))
#factorial(5)

#Defun { name: fibonacci, arguments: (n,) } (n == 0) ? (0) : (n == 1) ? (1) : (fibonacci(n - 1) + fibonacci(n - 2))
#fibonacci(6)
#fibonacci(0)
#fibonacci(1)

#Defun {name: sum_to_n, arguments: (n)} (n == 0) ? 0 : (n + sum_to_n(n - 1))
#sum_to_n(10)

#(Lambd x.(Lambd y.(x + y)))(factorial(5),5)
#(Lambd x.(Lambd y.(x + y)))(3,5)
#(x > 0) && (y < 10)
#(x > 0) && !(y < 10)
#(x == 3) && (y != 10)
#2+5*3


#Defun {name: apply_twice, arguments: (f,)} f+1
#apply_twice(Lambd x.(x + 1))(3)
