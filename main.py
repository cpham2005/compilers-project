from Lexer import *
from parser import *

def main():
    tests = [("test1.txt", "output1.txt"), ("test2.txt", "output2.txt"), ("test3.txt", "output3.txt")]

    for test, output in tests:
        with open(test, "r") as file:
            sourcecode = file.read()

        lexer = Lexer(sourcecode)
        parser = Parser(lexer)

        try:
            parser.rat26f()
        except SyntaxError as error:
            parser.output.append(f"Syntax Error: {error}")

    
        with open(output, "w") as file:
            for line in parser.output:
                file.write(line + "\n")
                
if __name__ == "__main__":
    main()