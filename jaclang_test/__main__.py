from os import listdir
from os.path import dirname

from jaclang import compileJaclang
from virtual_machine import VirtualMachine


def main():
    success_count = 0
    test_count = 0
    tests_dir = dirname(__file__) + "/tests/"
    for file in sorted(listdir(tests_dir)):
        if file.endswith(".jl"):
            with open(tests_dir + file, "r") as jl_file:
                file_contents = jl_file.read()
            lines = file_contents.split("\n")
            line_tokens = lines[0].split(" ")
            if len(line_tokens) != 3 or line_tokens[0:2] != ["///", "expect"]:
                continue
            expected_value = int(line_tokens[2])
            binary_code = compileJaclang(file_contents, [])
            virtual_machine = VirtualMachine(2**16)
            virtual_machine.run(binary_code)
            success = virtual_machine.getReturnCode() == expected_value
            test_count += 1
            if success:
                success_count += 1
            print(f"Testing {file} {len(binary_code)}B, {virtual_machine.getCycleCount()} cycles, ram used {virtual_machine.max_stack}B ... {'SUCCESS' if success else 'FAIL'}")
            if not success:
                print(f"Test failed: expected {expected_value} but got {virtual_machine.getReturnCode()}")
    print(f"Test results: {success_count} succeeded out of {test_count}")


if __name__ == "__main__":
    main()
