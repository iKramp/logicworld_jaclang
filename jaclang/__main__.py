import sys
import preprocessor
import lexer
import parser
import generator
import binary_writer


def main():
    """if len(sys.argv) != 2:
        print("Usage: python3 -m jaclang [input_file]")
        return

    input_file = sys.argv[1]

    with open(input_file, "r") as file:
        file_contents = file.read()

    preprocessed_contents = preprocessor.preprocess(file_contents)
    tokens = lexer.tokenize(preprocessed_contents)
    instructions = parser.parse(tokens)
    binary_code = generator.generate(instructions)"""

    binary_code = [0b00001101, 0b00000000, 0b10101010, 0b00000000,
                   0b00001101, 0b11111111, 0b01010101, 0b00000000]
    binary_writer.writeBinary(binary_code)


main()
