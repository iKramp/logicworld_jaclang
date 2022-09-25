from abc import abstractmethod


class Parameter:
    @abstractmethod
    def toBytes(self) -> list[int]:
        pass

    @abstractmethod
    def getInfo(self) -> str:
        pass


class RegisterParameter(Parameter):
    def __init__(self, register_number, name):
        self.register_number = register_number
        self.name = name

    def toBytes(self) -> list[int]:
        return [self.register_number]

    def getInfo(self) -> str:
        return self.name


REG0 = RegisterParameter(0, "REG0")
REG1 = RegisterParameter(1, "REG1")
REG2 = RegisterParameter(2, "REG2")
REG3 = RegisterParameter(3, "REG3")
REG4 = RegisterParameter(4, "REG4")
EXPR_REG = RegisterParameter(5, "EXPR_REG")
RET_REG = RegisterParameter(6, "RET_REG")
SB_REG = RegisterParameter(7, "SB_REG")


class Value16Parameter(Parameter):
    def __init__(self, value):
        self.value = value

    def toBytes(self) -> list[int]:
        return [self.value & 0xFF, (self.value << 8) & 0xFF]

    def getInfo(self) -> str:
        return str(self.value)


class Value8Parameter(Parameter):
    def __init__(self, value):
        self.value = value

    def toBytes(self) -> list[int]:
        return [self.value & 0xFF]

    def getInfo(self) -> str:
        return str(self.value)


class EmptyByteParameter(Parameter):
    def toBytes(self) -> list[int]:
        return [0]

    def getInfo(self) -> str:
        return ""


class Instruction:
    def __init__(self, name: str, opcode: int, params: list[Parameter], length: int):
        self.name = name
        self.opcode = opcode
        self.params = params
        self.length = length
        if length not in [0, 2, 4]:
            raise Exception("Instruction length must be either 0, 2 or 4")

    def printInfo(self):
        info = "    " + self.name + " "
        for param in self.params:
            info += param.getInfo() + " "
        print(info)

    def toBytes(self) -> list[int]:
        if self.length == 0:
            return []

        byte_arr = [self.opcode]
        for param in self.params:
            byte_arr += param.toBytes()

        if len(byte_arr) != self.length:
            raise Exception("Byte array length must match")

        return byte_arr


class NopInstruction(Instruction):
    def __init__(self):
        super().__init__("NOP", 0b00000, [EmptyByteParameter()], 2)


class AddInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("ADD", 0b00001, [reg_a, reg_b, reg_save], 4)


class SubInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("SUB", 0b00010, [reg_a, reg_b, reg_save], 4)


class BslInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("BSL", 0b00011, [reg_a, reg_b, reg_save], 4)


class BsrInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("BSR", 0b00100, [reg_a, reg_b, reg_save], 4)


class OrInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("OR", 0b00101, [reg_a, reg_b, reg_save], 4)


class AndInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("AND", 0b00111, [reg_a, reg_b, reg_save], 4)


class XorInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("XOR", 0b00110, [reg_a, reg_b, reg_save], 4)


class NotInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("NOT", 0b01000, [reg_a, EmptyByteParameter(), reg_save], 4)


class XnorInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("XNOR", 0b01001, [reg_a, reg_b, reg_save], 4)


class NandInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("NAND", 0b01010, [reg_a, reg_b, reg_save], 4)


class MemwInstruction(Instruction):
    def __init__(self, reg_addr: RegisterParameter, addr_offset: int, reg_value: RegisterParameter):
        super().__init__("MEMW", 0b01011, [reg_addr, reg_value, Value8Parameter(addr_offset)], 4)


class MemrInstruction(Instruction):
    def __init__(self, reg_addr: RegisterParameter, addr_offset: int, reg_save: RegisterParameter):
        super().__init__("MEMR", 0b01100, [reg_addr, Value8Parameter(addr_offset), reg_save], 4)


class ImmediateInstruction(Instruction):
    def __init__(self, reg_save: RegisterParameter, value: int):
        super().__init__("IMM", 0b01101, [reg_save, Value16Parameter(value)], 4)


class MovInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("MOV", 0b01110, [reg_a, EmptyByteParameter(), reg_save], 4)


class CmpInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, flags: int):
        super().__init__("CMP", 0b01111, [reg_a, reg_b, Value8Parameter(flags)], 4)


class JmpInstruction(Instruction):
    def __init__(self, address: int):
        super().__init__("JMP", 0b10000, [EmptyByteParameter(), Value16Parameter(address)], 4)


class GpuDrawInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter):
        super().__init__("GPU_DRAW", 0b10001, [reg_a, reg_b, EmptyByteParameter()], 4)


class GpuDisplayInstruction(Instruction):
    def __init__(self):
        super().__init__("GPU_DISPLAY", 0b10010, [EmptyByteParameter()], 2)


class PushInstruction(Instruction):
    def __init__(self, reg: RegisterParameter):
        super().__init__("PUSH", 0b10011, [reg], 2)


class PopInstruction(Instruction):
    def __init__(self, reg: RegisterParameter):
        super().__init__("POP", 0b10100, [reg], 2)


class SetSpInstruction(Instruction):
    def __init__(self, reg: RegisterParameter):
        super().__init__("SETSP", 0b10101, [reg], 2)


class GetSpInstruction(Instruction):
    def __init__(self, reg: RegisterParameter):
        super().__init__("GETSP", 0b10110, [EmptyByteParameter(), EmptyByteParameter(), reg], 4)


class GetPcInstruction(Instruction):
    def __init__(self, reg: RegisterParameter):
        super().__init__("GETPC", 0b10111, [EmptyByteParameter(), EmptyByteParameter(), reg], 4)


class PushaInstruction(Instruction):
    def __init__(self):
        super().__init__("PUSHA", 0b11000, [EmptyByteParameter()], 2)


class PopaInstruction(Instruction):
    def __init__(self):
        super().__init__("POPA", 0b11001, [EmptyByteParameter()], 2)


class CallInstruction(Instruction):
    def __init__(self, address: int):
        super().__init__("CALL", 0b11010, [EmptyByteParameter(), Value16Parameter(address)], 4)


class RetInstruction(Instruction):
    def __init__(self):
        super().__init__("RET", 0b11011, [EmptyByteParameter()], 2)


class LabelInstruction(Instruction):
    def __init__(self, label_name: str):
        super().__init__("", 0b00000, [], 0)
        self.label_name = label_name

    def printInfo(self):
        print(f"{self.label_name}:")


def generate(instructions: list[Instruction], debug_output: bool = False) -> list[int]:
    if debug_output:
        print("Generated assembly code:")
        print("---------------------------------")
        for instruction in instructions:
            instruction.printInfo()
        print("---------------------------------")
    binary_code = []
    for instruction in instructions:
        binary_code += instruction.toBytes()
    return binary_code
