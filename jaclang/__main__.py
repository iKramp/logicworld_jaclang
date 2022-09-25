import sys

from jaclang.error.syntaxError import JaclangSyntaxError
from jaclang.generator import generate
from jaclang.lexer import tokenize
from jaclang.parser import parse
from jaclang.preprocessor import preprocess


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 -m jaclang [input_file]")
        return

    input_file = sys.argv[1]

    with open(input_file, "r") as file:
        file_contents = file.read()

    try:
        preprocessed_contents = preprocess(file_contents, False)
        tokens = tokenize(preprocessed_contents, False)
        instructions = parse(tokens, True)
        binary_code = generate(instructions, True)

        print(f"Binary code size: {len(binary_code)} bytes")
    except JaclangSyntaxError as error:
        error.printError(file_contents)
        exit(1)

    # binary_writer.writeBinary(binary_code)


main()
