from enum import Enum

class TokenT(Enum):
    EOF = "EOF"         # end of file
    SEPARATOR = "SEPARATOR"
    OPERATOR = "OPERATOR"
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    UNKNOWN = "UNKNOWN"         # unrecognizable
    INTEGER = "INTEGER"
    REAL = "REAL"

SEPARATORS = {":", ";", "(", ")", "@", ",", "_", "{", "}"}
OPERATORS = {"==", "!=", ">", "<", "<=", ">=", "+", "-", "*", "/"}
KEYWORDS = {"true", "false", "if", "put", "return", "get", "integer",
            "Boolean", "real", "while", "fi", "else"}

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.pos = 0                # position in text
        self.char = ""              # specific character in text

        self.read_char()

    def read_char(self):
        if self.pos >= len(self.source):
            self.char = ""          # signals end of the text; might need to edit
        else:
            self.char = self.source[self.pos]     #character is what the code is in that pos
            self.pos += 1           # move position one over (should i separate update/read and moving)

    def read_word(self):
        text = ""           # place to store word
        while self.char != "" and self.char.isalnum():      # find where word start; alphanumeric
            text += self.char           # start adding characters of word to text
            self.read_char()            # keep moving
        if text in KEYWORDS:
            return Token(TokenT.KEYWORD, text)
        return Token(TokenT.IDENTIFIER, text)

    def read_operator(self):
        initial = self.char       # save current character
        self.read_char()    #before moving^

        if initial in ("=", "!", "<", ">") and self.char == "=":  # manually check only operators 
            self.read_char()
            return Token(TokenT.OPERATOR, initial + "=")      # return prev char and = 
        
        if initial in ("<", ">", "+", "-", "*", "/", "="):
            return Token(TokenT.OPERATOR, initial)

        if initial == "!":
            while self.char != "" and self.char != "!":     # comments enclosed with ! are skipped
                self.read_char()        # skip character inside !
            self.read_char()            # skip the last !
            return self.next_token()    # return no name token since comment are not labeled
            
        return Token(TokenT.UNKNOWN, initial)      # come back when working on comments

    def skip_space(self):
        while self.char != "" and self.char.isspace():  #skip whitespace
            self.read_char()

    def read_number(self):
        text = ""
        while self.char != "" and self.char.isdigit():
            text += self.char
            self.read_char()
        if self.char == ".":
            text += self.char
            self.read_char()
            if self.char == "" or not self.char.isdigit():
                return Token(TokenT.UNKNOWN, text)

            while self.char != "" and self.char.isdigit():
                text += self.char
                self.read_char()
        if "." in text:
            return Token(TokenT.REAL, text)
        return Token(TokenT.INTEGER, text)

# looping and labeling characters
    def next_token(self):
        self.skip_space()   # default skip whitespace

        if self.char == "":
            return Token(TokenT.EOF, "")        #check for end of file
        
        # if not end of file then label
        if self.char.isalpha():                 # checking for words (identifiers and keywords)
            return self.read_word()

        if self.char.isdigit() or self.char == ".":     #check for real and interger
            return self.read_number()

        if self.char in ("=", "!", "<", ">", "+", "-", "*", "/"):
            return self.read_operator()

        if self.char in SEPARATORS:
            tok = Token(TokenT.SEPARATOR, self.char)
        else:
            tok = Token(TokenT.UNKNOWN, self.char)

        self.read_char()            # just keep moving
        return tok