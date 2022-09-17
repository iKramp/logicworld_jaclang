from jaclang.generator import Instruction
from jaclang.lexer import Token
from jaclang.parser.function import FunctionDeclarationBranch
from jaclang.parser.root import RootFactory


def parse(tokens: list[Token], debug_output: bool = False) -> list[Instruction]:
    root_factory = RootFactory()

    _, root_branch = root_factory.parseImpl(0, tokens)

    if debug_output:
        print("Generated abstract syntax tree:")
        print("---------------------------------")
        root_branch.printInfo(0)
        print("---------------------------------")

    return root_branch.generateInstructions()
