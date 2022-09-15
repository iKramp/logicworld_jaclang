import sys
import preprocessor
import lexer
import parser
import generator


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 -m jaclang [input_file] [output_file]")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, "r") as file:
        file_contents = file.read()

    preprocessed_contents = preprocessor.preprocess(file_contents)
    tokens = lexer.tokenize(preprocessed_contents)
    instructions = parser.parse(tokens)
    binary_code = generator.generate(instructions)

    with open(output_file, "wb") as file:
        file.write(binary_code)


main()
