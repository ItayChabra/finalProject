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
#(Lambd x.(Lambd y.(x + y)))(factorial(5),5)
#(Lambd x.(Lambd y.(x + y)))(3,5)
#(x > 0) && (y < 10)
#(x > 0) && !(y < 10)
#(x == 3) && (y != 10)
#2+5*3
#Defun {name : fibonacci, arguments : (n,) } (n == 0) || (n == 1) || (fibonacci(n - 1) + fibonacci(n - 2))
#Defun {name: apply_twice, arguments: (f, x)} f(f(x))
#Defun {name: apply_twice, arguments: (f,)} Lambd x.(f(f(x)))
#apply_twice(Lambd x.(x + 1))(3)