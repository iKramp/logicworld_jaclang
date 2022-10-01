import sys

from jaclang import compileJaclang
from jaclang.error.syntax_error import JaclangSyntaxError


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
    except JaclangSyntaxError as error:
        error.printError(file_contents)
        exit(1)

    # binary_writer.writeBinary(binary_code)


if __name__ == "__main__":
    main()
