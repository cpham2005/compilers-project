from Lexer import *

def main():
    test1 = "test2.txt"
    with open(test1, "r") as file:
        sourcecode = file.read()

    lexer = Lexer(sourcecode)

    while True:
        token = lexer.next_token()
        if token.type == TokenT.EOF:
            break
        print(token.type.value, token.value)

if __name__ == "__main__":
    main()