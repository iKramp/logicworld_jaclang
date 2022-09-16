import generator
import lexer


def parse(tokens: list[lexer.Token], debug_output: bool = False) -> list[generator.Instruction]:
    instructions = []
    if debug_output:
        print("Generated abstract syntax tree:")
        print("---------------------------------")
        for instruction in instructions:
            instruction.printInfo()
        print("---------------------------------")
    return instructions
