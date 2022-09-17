from abc import abstractmethod


class Token:
    @abstractmethod
    def getInfo(self) -> str:
        pass


class SymbolToken(Token):
    symbols = []

    def __init__(self, name: str, identifier: str):
        self.name = name
        self.identifier = identifier
        SymbolToken.symbols.append(self)

    def getInfo(self) -> str:
        return self.name


class IdentifierToken(Token):
    def __init__(self, identifier: str):
        self.identifier = identifier

    def getInfo(self) -> str:
        return f"ident: {self.identifier}"


LEFT_BRACKET = SymbolToken("LEFT_BRACKET", "(")
RIGHT_BRACKET = SymbolToken("RIGHT_BRACKET", ")")
ASSIGNMENT = SymbolToken("ASSIGNMENT", "=")
EQUAL = SymbolToken("EQUAL", "==")
LESS_THAN = SymbolToken("LESS_THAN", "<")
GREATER_THAN = SymbolToken("GREATER_THAN", ">")
LESS_OR_EQUAL_THAN = SymbolToken("LESS_OR_EQUAL_THAN", "<=")
GREATER_OR_EQUAL_THAN = SymbolToken("GREATER_OR_EQUAL_THAN", ">=")
NOT_EQUAL = SymbolToken("NOT_EQUAL", "!=")
AND = SymbolToken("AND", "&")
NAND = SymbolToken("NAND", "!&")
OR = SymbolToken("OR", "|")
XOR = SymbolToken("XOR", "^")
LEFT_BRACE = SymbolToken("LEFT_BRACE", "{")
RIGHT_BRACE = SymbolToken("RIGHT_BRACE", "}")
SQUARE_LEFT_BRACKET = SymbolToken("SQUARE_LEFT_BRACKET", "[")
SQUARE_RIGHT_BRACKET = SymbolToken("SQUARE_RIGHT_BRACKET", "]")
INCREMENT = SymbolToken("INCREMENT", "++")
DECREMENT = SymbolToken("DECREMENT", "--")
INCREMENT_BY = SymbolToken("INCREMENT_BY", "+=")
DECREMENT_BY = SymbolToken("DECREMENT_BY", "-=")


def tokenize(code: str, debug_output: bool = False) -> list[Token]:
    tokens = []
    curr_token = ""

    i = 0
    while i < len(code):
        curr_symbol = None
        for symbol in SymbolToken.symbols:
            if code.startswith(symbol.identifier, i):
                curr_symbol = symbol

        if code[i] == ' ' or curr_symbol is not None:
            if curr_token != "":
                new_token = IdentifierToken(curr_token)
                curr_token = ""
                tokens.append(new_token)

            if code[i] == ' ':
                i += 1

            if curr_symbol is not None:
                tokens.append(curr_symbol)
                i += len(curr_symbol.identifier)
        else:
            curr_token += code[i]
            i += 1

    if debug_output:
        print("Generated tokens:")
        print("---------------------------------")
        for token in tokens:
            print(token.getInfo())
        print("---------------------------------")
    return tokens
