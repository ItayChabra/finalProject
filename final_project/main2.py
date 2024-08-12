from my_interpreter import Interpreter

def main():
    if len(sys.argv) > 1:
        # Run the interpreter with a program file
        file_path = sys.argv[1]
        interpreter = Interpreter()
        interpreter.run_program(file_path)
    else:
        # Run the interpreter in interactive mode
        interpreter = Interpreter()
        interpreter.repl()

if __name__ == "__main__":
    main()

#Defun { name: factorial, arguments: (n,) } (n == 0) || (n * factorial(n - 1))