import sys
import preprocessor
import lexer
import parser
import generator
import binary_writer


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 -m jaclang [input_file]")
        return

    input_file = sys.argv[1]

    with open(input_file, "r") as file:
        file_contents = file.read()

    preprocessed_contents = preprocessor.preprocess(file_contents, True)
    tokens = lexer.tokenize(preprocessed_contents)
    instructions = parser.parse(tokens)

    """instructions = [
        generator.ImmediateInstruction(generator.REG0, 0b11011),
        generator.ImmediateInstruction(generator.REG1, 0b00111),
        generator.AddInstruction(generator.REG0, generator.REG1, generator.REG2),
        generator.NopInstruction(),
    ]"""
    binary_code = generator.generate(instructions, True)

    print(f"Binary code size: {len(binary_code)} bytes")

    # binary_writer.writeBinary(binary_code)


main()
