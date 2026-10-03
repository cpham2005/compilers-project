from Lexer import *

def main():
    tests = [("test1.txt", "output1.txt"), ("test2.txt", "output2.txt"), ("test3.txt", "output3.txt")]

    for test, output in tests:
        with open(test, "r") as file:
            sourcecode = file.read()

        lexer = Lexer(sourcecode)

        with open(output, "w") as file:
            while True:
                token = lexer.next_token()
                if token.type == TokenT.EOF:
                    break

                file.write(f"{token.type.value} {token.value}\n")

if __name__ == "__main__":
    main()