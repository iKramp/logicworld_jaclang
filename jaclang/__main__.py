import sys

from jaclang.error.syntaxError import JaclangSyntaxError
from jaclang.generator import generate
from jaclang.lexer import tokenize
from jaclang.parser import parse
from jaclang.preprocessor import preprocess


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
        preprocessed_contents = preprocess(file_contents, "debug_preprocess" in options)
        tokens = tokenize(preprocessed_contents, "debug_tokens" in options)
        instructions = parse(tokens, "debug_tree" in options)
        binary_code = generate(instructions, "debug_assembly" in options)

        print(f"Binary code size: {len(binary_code)} bytes")
    except JaclangSyntaxError as error:
        error.printError(file_contents)
        exit(1)

    # binary_writer.writeBinary(binary_code)


main()
