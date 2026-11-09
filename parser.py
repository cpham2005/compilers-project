
from Lexer import *

class Parser:
    def __init__(self, lexer):=
        self.lexer = lexer
        self.current_token = None
        self.output = []

    def next_token(self):=
        self.current_token = self.lexer.next_token()

        if self.current_token.type != TokenT.EOF:
            self.output.append(
                f"Token: {self.current_token.type.value} "
                f"Lexeme: {self.current_token.value}"
            )

        return self.current_token

    def production(self, text):
        self.output.append(text)

    # R1
    def rat26f(self):
        self.next_token()
        self.production("<Rat26F> -> <Opt Function Definitions> @ <Opt Declaration List> @ <Statement List>")

        self.opt_function_definitions()

        if self.current_token is not None and self.current_token.value == "@":
            self.next_token()
        else:
            raise SyntaxError("Expected @")

        self.opt_declaration_list()

        if self.current_token is not None and self.current_token.value == "@":
            self.next_token()
        else:
            raise SyntaxError("Expected @")

        self.statement_list()

        if self.current_token.type != TokenT.EOF:
            raise SyntaxError("Unexpected input after program")

    # R2
    def opt_function_definitions(self):
        if self.current_token.value == "function":
            self.production("<Opt Function Definitions> -> <Function Definitions>")
            self.function_definitions()
        else:
            self.production("<Opt Function Definitions> -> <Empty>")
            self.empty()

    # R3
    def function_definitions(self):
        self.function()

        if self.current_token.value == "function":
            self.production("<Function Definitions> -> <Function> <Function Definitions>")
            self.function_definitions()
        else:
            self.production("<Function Definitions> -> <Function>")

    # R4
    def function(self):
        self.production("<Function> -> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
        self.next_token()

        if self.current_token.type == TokenT.IDENTIFIER:
            self.next_token()
        else:
            raise SyntaxError("Expected identifier")

        if self.current_token.value == "(":
            self.next_token()
        else:
            raise SyntaxError("Expected (")

        self.opt_parameter_list()

        if self.current_token.value == ")":
            self.next_token()
        else:
            raise SyntaxError("Expected )")

        self.opt_declaration_list()
        self.body()

    # R5
    def opt_parameter_list(self):
        if self.current_token.type == TokenT.IDENTIFIER:
            self.production("<Opt Parameter List> -> <Parameter List>")
            self.parameter_list()
        else:
            self.production("<Opt Parameter List> -> <Empty>")
            self.empty()

    # R6
    def parameter_list(self):
        self.parameter()

        if self.current_token.value == ",":
            self.production("<Parameter List> -> <Parameter> , <Parameter List>")
            self.next_token()
            self.parameter_list()
        else:
            self.production("<Parameter List> -> <Parameter>")

    # R7
    def parameter(self):
        self.production("<Parameter> -> <IDs> <Qualifier>")
        self.ids()
        self.qualifier()

    # R8
    def qualifier(self):
        self.production("<Qualifier> -> integer | boolean | real")

        if self.current_token.value in ["integer", "boolean", "real"]:
            self.next_token()
        else:
            raise SyntaxError("Expected qualifier")

    # R9
    def body(self):
        self.production("<Body> -> { <Statement List> }")

        if self.current_token.value == "{":
            self.next_token()
        else:
            raise SyntaxError("Expected {")

        self.statement_list()

        if self.current_token.value == "}":
            self.next_token()
        else:
            raise SyntaxError("Expected }")

    # R10
    def opt_declaration_list(self):
        if self.current_token.value in ["integer", "boolean", "real"]:
            self.production("<Opt Declaration List> -> <Declaration List>")
            self.declaration_list()
        else:
            self.production("<Opt Declaration List> -> <Empty>")
            self.empty()

    # R11
    def declaration_list(self):
        self.declaration()

        if self.current_token.value == ";":
            self.next_token()
        else:
            raise SyntaxError("Expected ;")

        if self.current_token.value in ["integer", "boolean", "real"]:
            self.production("<Declaration List> -> <Declaration> ; <Declaration List>")
            self.declaration_list()
        else:
            self.production("<Declaration List> -> <Declaration> ;")

    # R12
    def declaration(self):
        self.production("<Declaration> -> <Qualifier> <IDs>")
        self.qualifier()
        self.ids()

    # R13
    def ids(self):
        if self.current_token.type == TokenT.IDENTIFIER:
            self.next_token()
        else:
            raise SyntaxError("Expected identifier")

        if self.current_token.value == ",":
            self.production("<IDs> -> <Identifier> , <IDs>")
            self.next_token()
            self.ids()
        else:
            self.production("<IDs> -> <Identifier>")

    # R14
    def statement_list(self):
        self.statement()

        if self.current_token is not None and (
            self.current_token.type == TokenT.IDENTIFIER or
            self.current_token.value in ["{", "if", "return", "put", "get", "while"]
        ):
            self.production("<Statement List> -> <Statement> <Statement List>")
            self.statement_list()
        else:
            self.production("<Statement List> -> <Statement>")

    # R15
    def statement(self):
        if self.current_token.type == TokenT.IDENTIFIER:
            self.production("<Statement> -> <Assign>")
            self.assign()
        elif self.current_token.value == "{":
            self.production("<Statement> -> <Compound>")
            self.compound()
        elif self.current_token.value == "if":
            self.production("<Statement> -> <If>")
            self.p_if()
        elif self.current_token.value == "return":
            self.production("<Statement> -> <Return>")
            self.p_return()
        elif self.current_token.value == "put":
            self.production("<Statement> -> <Print>")
            self.p_print()
        elif self.current_token.value == "get":
            self.production("<Statement> -> <Scan>")
            self.scan()
        elif self.current_token.value == "while":
            self.production("<Statement> -> <While>")
            self.p_while()
        else:
            raise SyntaxError("Expected Statement")

    # R16
    def compound(self):
        self.production("<Compound> -> { <Statement List> }")

        if self.current_token.value == "{":
            self.next_token()
        else:
            raise SyntaxError("Expected {")

        self.statement_list()

        if self.current_token.value == "}":
            self.next_token()
        else:
            raise SyntaxError("Expected }")

    # R17
    def assign(self):
        self.production("<Assign> -> <Identifier> = <Expression> ;")

        if self.current_token.type == TokenT.IDENTIFIER:
            self.next_token()
        else:
            raise SyntaxError("Expected identifier")

        if self.current_token.value == "=":
            self.next_token()
        else:
            raise SyntaxError("Expected =")

        self.expression()

        if self.current_token.value == ";":
            self.next_token()
        else:
            raise SyntaxError("Expected ;")

    # R18
    def p_if(self):
        if self.current_token.value == "if":
            self.next_token()
        else:
            raise SyntaxError("Expected if")

        if self.current_token.value == "(":
            self.next_token()
        else:
            raise SyntaxError("Expected (")

        self.condition()

        if self.current_token.value == ")":
            self.next_token()
        else:
            raise SyntaxError("Expected )")

        self.statement()

        if self.current_token.value == "else":
            self.production("<If> -> if ( <Condition> ) <Statement> else <Statement> fi")
            self.next_token()
            self.statement()
        else:
            self.production("<If> -> if ( <Condition> ) <Statement>")

        if self.current_token.value == "fi":
            self.next_token()
        else:
            raise SyntaxError("Expected fi")

    # R19
    def p_return(self):
        if self.current_token.value == "return":
            self.next_token()
        else:
            raise SyntaxError("Expected return")

        if self.current_token.value != ";":
            self.production("<Return> -> return <Expression> ;")
            self.expression()
        else:
            self.production("<Return> -> return ;")

        if self.current_token.value == ";":
            self.next_token()
        else:
            raise SyntaxError("Expected ;")

    # R20
    def p_print(self):
        self.production("<Print> -> put ( <Expression> ) ;")

        if self.current_token.value == "put":
            self.next_token()
        else:
            raise SyntaxError("Expected put")

        if self.current_token.value == "(":
            self.next_token()
        else:
            raise SyntaxError("Expected (")

        self.expression()

        if self.current_token.value == ")":
            self.next_token()
        else:
            raise SyntaxError("Expected )")

        if self.current_token.value == ";":
            self.next_token()
        else:
            raise SyntaxError("Expected ;")

    # R21
    def scan(self):
        self.production("<Scan> -> get ( <IDs> ) ;")

        if self.current_token.value == "get":
            self.next_token()
        else:
            raise SyntaxError("Expected get")

        if self.current_token.value == "(":
            self.next_token()
        else:
            raise SyntaxError("Expected (")

        self.ids()

        if self.current_token.value == ")":
            self.next_token()
        else:
            raise SyntaxError("Expected )")

        if self.current_token.value == ";":
            self.next_token()
        else:
            raise SyntaxError("Expected ;")

    # R22
    def p_while(self):
        self.production("<While> -> while ( <Condition> ) <Statement>")

        if self.current_token is not None and self.current_token.value == "while":
            self.next_token()
        else:
            raise SyntaxError("Expected while")

        if self.current_token is not None and self.current_token.value == "(":
            self.next_token()
        else:
            raise SyntaxError("Expected (")

        self.condition()

        if self.current_token is not None and self.current_token.value == ")":
            self.next_token()
        else:
            raise SyntaxError("Expected )")

        if self.current_token is None or self.current_token.type == TokenT.EOF:
            raise SyntaxError("Expected Statement")

        self.statement()

    # R23
    def condition(self):
        self.production("<Condition> -> <Expression> <Relop> <Expression>")
        self.expression()
        self.relop()
        self.expression()

    # R24
    def relop(self):
        if self.current_token is not None and self.current_token.value in ["==", "!=", ">", "<", "<=", ">="]:
            self.production("<Relop> -> == | != | > | < | <= | >=")
            self.next_token()
        else:
            raise SyntaxError("Expected relational operator")

    # R25a
    def expression(self):
        self.production("<Expression> -> <Term> <Expression Prime>")
        self.term()
        self.expression_prime()

    # R25b
    def expression_prime(self):
        if self.current_token is not None and self.current_token.value == "+":
            self.production("<Expression Prime> -> + <Term> <Expression Prime>")
            self.next_token()
            self.term()
            self.expression_prime()

        elif self.current_token is not None and self.current_token.value == "-":
            self.production("<Expression Prime> -> - <Term> <Expression Prime>")
            self.next_token()
            self.term()
            self.expression_prime()

        else:
            self.production("<Expression Prime> -> <Empty>")
            self.empty()

    # R26a
    def term(self):
        self.production("<Term> -> <Factor> <Term Prime>")
        self.factor()
        self.term_prime()

    # R26b
    def term_prime(self):
        if self.current_token is not None and self.current_token.value == "*":
            self.production("<Term Prime> -> * <Factor> <Term Prime>")
            self.next_token()
            self.factor()
            self.term_prime()

        elif self.current_token is not None and self.current_token.value == "/":
            self.production("<Term Prime> -> / <Factor> <Term Prime>")
            self.next_token()
            self.factor()
            self.term_prime()

        else:
            self.production("<Term Prime> -> <Empty>")
            self.empty()

    # R27
    def factor(self):
        if self.current_token is not None and self.current_token.value == "-":
            self.production("<Factor> -> - <Primary>")
            self.next_token()
        else:
            self.production("<Factor> -> <Primary>")

        self.primary()

    # R28
    def primary(self):
        if self.current_token is None or self.current_token.type == TokenT.EOF:
            raise SyntaxError("Expected primary")

        if self.current_token.type == TokenT.IDENTIFIER:
            self.next_token()

            if self.current_token is not None and self.current_token.value == "(":
                self.production("<Primary> -> <Identifier> ( <IDs> )")
                self.next_token()
                self.ids()

                if self.current_token is not None and self.current_token.value == ")":
                    self.next_token()
                else:
                    raise SyntaxError("Expected )")
            else:
                self.production("<Primary> -> <Identifier>")

        elif self.current_token.type == TokenT.INTEGER:
            self.production("<Primary> -> <Integer>")
            self.next_token()

        elif self.current_token.type == TokenT.REAL:
            self.production("<Primary> -> <Real>")
            self.next_token()

        elif self.current_token.value in ["true", "false"]:
            self.production("<Primary> -> true | false")
            self.next_token()

        elif self.current_token.value == "(":
            self.production("<Primary> -> ( <Expression> )")
            self.next_token()
            self.expression()

            if self.current_token is not None and self.current_token.value == ")":
                self.next_token()
            else:
                raise SyntaxError("Expected )")

        else:
            raise SyntaxError("Expected primary")

    # R29
    def empty(self):
        self.production("<Empty> -> ε")
