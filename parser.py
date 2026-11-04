from lexer import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.token_index = 0

    def next_token(self):
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
            self.token_index += 1
        else:
            self.current_token = None
        return self.current_token  

    # R1
    def rat26f(self):
        self.next_token()

        self.opt_function_definitions()

        if self.current_token.value == "@" and self.current_token is not None:
            self.next_token()
        else:
            raise SyntaxError("Expected @")
        
        self.opt_declaration_list()

        if self.current_token.value == "@" and self.current_token is not None:
            self.next_token()
        else:
            raise SyntaxError("Expected @")

        self.statement_list()

    # R2
    def opt_function_definitions(self):
        if self.current_token.value == "function":
            self.function_definitions()
        else:
            self.empty()

    # R3
    def function_definitions(self):
        self.function()

        if self.current_token.value == "function":
            self.function_definitions()

    # R4
    def function(self):
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
            self.parameter_list()
        else:
            self.empty()

    
    # R6
    def parameter_list(self):
        self.parameter()

        if self.current_token.value == ",":
            self.next_token()
            self.parameter_list()

    # R7
    def parameter(self):
        self.ids()
        self.qualifier()

    # R8
    def qualifier(self):
        if self.current_token.value in ["integer", "Boolean", "real"]:
            self.next_token()
        else:
            raise SyntaxError("Expected qualifier")

    # R9
    def body(self):
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
        if self.current_token.value in ["integer", "Boolean", "real"]:
            self.declaration_list()
        else:
            self.empty()

    # R11
    def declaration_list(self):
        self.declaration()

        if self.current_token.value == ";":
            self.next_token()
        else:
            raise SyntaxError("Expected ;")

        if self.current_token.value in ["integer", "Boolean", "real"]:
            self.declaration_list()

    # R12
    def declaration(self):
        self.qualifier()
        self.ids()

    # R13
    def ids(self):
        if self.current_token.type == TokenT.IDENTIFIER:
            self.next_token()
        else:
            raise SyntaxError("Expected identifier")

        if self.current_token.value == ",":
            self.next_token()
            self.ids()

    # R14
    def statement_list(self):
        self.statement()

        if self.current_token is not None and (self.current_token.type == TokenT.IDENTIFIER or self.current_token.value in ["{", "if", "return", "put", "get", "while"]):
            self.statement_list()

    # R15
    def statement(self):
        if self.current_token.type == TokenT.IDENTIFIER:
            self.assign()
        elif self.current_token.value == "{":
            self.compound()
        elif self.current_token.value == "if":
            self.p_if()
        elif self.current_token.value == "return":
            self.p_return()
        elif self.current_token.value == "put":
            self.p_print()
        elif self.current_token.value == "get":
            self.scan()
        elif self.current_token.value == "while":
            self.p_while()
        else:
            raise SyntaxError("Expected Statement")

    # R16
    def compound(self):
        if self.current_token.value =="{":
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
            self.next_token()
            self.statement()

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
            self.expression()

        if self.current_token.value == ";":
            self.next_token()
        else:
            raise SyntaxError("Expected ;")
 

    # R20
    def p_print(self):
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
        pass

    # R23
    def condition(self):
        pass

    # R24
    def relop(self):
        pass

    # R25a
    def expression(self):
        pass

    # R25b
    def expression_prime(self):
        pass
    
    # R26a
    def term(self):
        pass

    # R26b
    def term_prime(self):
        pass

    # R27
    def factor(self):
        pass

    # R28
    def primary(self):
        pass

    # R29
    def empty(self):
        pass
