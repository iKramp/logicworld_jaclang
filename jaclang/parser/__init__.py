from jaclang.generator import Instruction
from jaclang.lexer import Token


def parse(tokens: list[Token], debug_output: bool = False) -> list[Instruction]:
    branches = [

    ]

    i = 0
    while i < len(tokens):
        for branch in branches:
            i = branch.parse(i)

    if debug_output:
        print("Generated abstract syntax tree:")
        print("---------------------------------")

        print("---------------------------------")
    instructions = []
    return instructions
