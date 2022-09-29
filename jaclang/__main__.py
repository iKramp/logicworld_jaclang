import sys

from jaclang.error.syntax_error import JaclangSyntaxError
from jaclang.generator import generate
from jaclang.lexer import tokenize
from jaclang.parser import parse
from jaclang.preprocessor import preprocess
from jaclang.virtual_machine import VirtualMachine


def compileJaclang(file_contents: str, options: list[str]) -> list[int]:
    preprocessed_contents = preprocess(file_contents, "debug_preprocess" in options)
    tokens = tokenize(preprocessed_contents, "debug_tokens" in options)
    instructions = parse(tokens, "debug_tree" in options)
    return generate(instructions, "debug_assembly" in options)


def main():
    if len(sys.argv) < 2:
        print(
            """Usage: python3 -m jaclang [input_file] [options]
Options:
- debug_preprocess: print preprocessed code
- debug_tokens: print tokens
- debug_tree: print abstract syntax tree
- debug_assembly: print generated assembly code"""
        )
        return

    input_file = sys.argv[1]
    options = sys.argv[2:]

    with open(input_file, "r") as file:
        file_contents = file.read()

    try:
        binary_code = compileJaclang(file_contents, options)

        print(f"Binary code size: {len(binary_code)} bytes")

        virtual_machine = VirtualMachine(256 * 4)
        virtual_machine.run(binary_code)

        print(f"Program returned {virtual_machine.getReturnCode()}")
        print(f"Cycles made: {virtual_machine.getCycleCount()}")
    except JaclangSyntaxError as error:
        error.printError(file_contents)
        exit(1)

    # binary_writer.writeBinary(binary_code)


if __name__ == "__main__":
    main()
