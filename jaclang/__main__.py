import sys

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

    preprocessed_contents = preprocess(file_contents, True)
    tokens = tokenize(preprocessed_contents, True)
    instructions = parse(tokens, True)

    binary_code = generate(instructions, True)

    print(f"Binary code size: {len(binary_code)} bytes")

    # binary_writer.writeBinary(binary_code)


main()
