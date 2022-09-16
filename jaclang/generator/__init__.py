from abc import abstractmethod


class Parameter:
    @abstractmethod
    def toBytes(self) -> list[int]:
        pass

    @abstractmethod
    def getInfo(self) -> str:
        pass


REGISTER_NAMES = ["REG0", "REG1", "REG2", "REG3", "REG4", "REG5", "REG6", "REG7"]


class RegisterParameter(Parameter):
    def __init__(self, register_number):
        self.register_number = register_number

    def toBytes(self) -> list[int]:
        return [self.register_number]

    def getInfo(self) -> str:
        return REGISTER_NAMES[self.register_number]


REG0 = RegisterParameter(0)
REG1 = RegisterParameter(1)
REG2 = RegisterParameter(2)
REG3 = RegisterParameter(3)
REG4 = RegisterParameter(4)
REG5 = RegisterParameter(5)
REG6 = RegisterParameter(6)
REG7 = RegisterParameter(7)


class ValueParameter(Parameter):
    def __init__(self, value):
        self.value = value

    def toBytes(self) -> list[int]:
        return [self.value & 0xFF, (self.value << 8) & 0xFF]

    def getInfo(self) -> str:
        return str(self.value)


class Instruction:
    def __init__(self, name: str, opcode: int, params: list[Parameter]):
        self.name = name
        self.opcode = opcode
        self.params = params

    def printInfo(self):
        info = self.name + " "
        for param in self.params:
            info += param.getInfo() + " "
        print(info)

    def toBytes(self) -> list[int]:
        byte_arr = [self.opcode]
        for param in self.params:
            byte_arr += param.toBytes()

        if len(byte_arr) not in [2, 4]:
            raise Exception("Byte array length must be either 4 or 2")

        return byte_arr


class ImmediateInstruction(Instruction):
    def __init__(self, reg_save: RegisterParameter, value: int):
        super().__init__("IMM", 0b01101, [reg_save, ValueParameter(value)])


class AddInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("ADD", 0b00001, [reg_a, reg_b, reg_save])


class NopInstruction(Instruction):
    def __init__(self):
        super().__init__("NOP", 0b00000, [RegisterParameter(0)])


def generate(instructions: list[Instruction], debug_output: bool = False):
    if debug_output:
        for instruction in instructions:
            instruction.printInfo()
    binary_code = []
    for instruction in instructions:
        binary_code += instruction.toBytes()
    return binary_code
