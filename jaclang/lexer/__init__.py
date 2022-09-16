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


LEFT_BRACKET = SymbolToken("LEFT_BRACE", "(")
RIGHT_BRACKET = SymbolToken("RIGHT_BRACE", ")")
ASSIGNMENT = SymbolToken("ASSIGNMENT", "=")
EQUAL = SymbolToken("EQUAL", "==")
LESS_THAN = SymbolToken("LESS_THAN", "<")
GRETER_THAN = SymbolToken("GRETER_THAN", ">")
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
    if debug_output:
        print("Generated tokens:")
        print("---------------------------------")

        print("---------------------------------")
    return tokens
