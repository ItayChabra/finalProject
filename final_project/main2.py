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
#Defun { name: factorial, arguments: (n,) } ((n == 0) ? 1 : (n * factorial(n - 1)))
#factorial(5)

#Defun { name: fibonacci, arguments: (n,) } (n == 0) ? (0) : (n == 1) ? (1) : (fibonacci(n - 1) + fibonacci(n - 2))
#fibonacci(6)

#Defun {name: sum_to_n, arguments: (n)} (n == 0) ? 0 : (n + sum_to_n(n - 1))
#sum_to_n(10)

#Defun { name: sum_of_digits, arguments: (n,) } (n < 10) ? n : (n % 10 + sum_of_digits(n / 10))
#sum_of_digits(123)

#Defun { name: check_positive, arguments: (x,) } (x > 0) ? TRUE : FALSE
#check_positive(5)
#check_positive(-3)

#(Lambd x.(Lambd y.(x + y)))(factorial(5),5)
#(Lambd x.(Lambd y.(x + y)))(3,5)
#(Lambd x.(Lambd y.(Lambd z. (x + y + z))))(1, 2, 3)
#(Lambd t.(Lambd x.(Lambd y.(Lambd z. (x + y + z + t)))))(1, 2, 3, 4)

#(x > 0) && (y < 10)
#(x > 0) && !(y < 10)
#(x == 3) && (y != 10)


#2+5*3

#Defun {name: plus_one, arguments: (f,)} f+1
#plus_one((Lambd x.(x + 1))(3))

