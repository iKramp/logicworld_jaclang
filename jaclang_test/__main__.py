from os import listdir, getcwd
from os.path import dirname

from jaclang import compileJaclang
from jaclang.virtual_machine import VirtualMachine


def main():
    for file in listdir(dirname(__file__)):
        if file.endswith(".jl"):
            with open(dirname(__file__) + "/" + file, "r") as jl_file:
                file_contents = jl_file.read()
            binary_code = compileJaclang(file_contents, [])
            virtual_machine = VirtualMachine(256 * 4)
            virtual_machine.run(binary_code)
            print(f"Testing {file} with return code {virtual_machine.getReturnCode()}")


if __name__ == "__main__":
    main()
