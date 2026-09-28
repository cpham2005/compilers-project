from enum import Enum

class TokenT(Enum):
    EOF = "EOF"         # end of file
    SEPARATOR = "SEPARATOR"
    UNKNOWN = "UNKNOWN"         # unrecognizable

SEPARATORS = {";", "(", ")", "@", ","}

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

    def skip_space(self):
        while self.char != "" and self.char.isspace():  #skip whitespace
            self.read_char()

# looping and labeling characters
    def next_token(self):
        self.skip_space()   # default skip whitespace

        if self.char == "":
            return Token(TokenT.EOF, "")        #check for end of file
        
        # if not end of file then label 
        elif self.char in SEPARATORS:
            tok = Token(TokenT.SEPARATOR, self.char)
        else:
            tok = Token(TokenT.UNKNOWN, self.char)
        self.read_char()
        
        return tok