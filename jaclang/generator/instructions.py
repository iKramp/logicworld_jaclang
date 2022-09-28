from jaclang.error.syntax_error import JaclangSyntaxError
from jaclang.generator import Instruction, EmptyByteParameter, RegisterParameter, Value16Parameter, Value8Parameter


class NopInstruction(Instruction):
    def __init__(self):
        super().__init__("NOP", 0b00000, [EmptyByteParameter()], 2)


class AddInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("ADD", 0b00001, [reg_a, reg_b, reg_save], 4)
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_save = reg_save

    def printInfo(self):
        print(f"    {self.reg_save.getInfo()} = {self.reg_a.getInfo()} + {self.reg_b.getInfo()}")


class SubInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("SUB", 0b00010, [reg_a, reg_b, reg_save], 4)
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_save = reg_save

    def printInfo(self):
        print(f"    {self.reg_save.getInfo()} = {self.reg_a.getInfo()} - {self.reg_b.getInfo()}")


class BslInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("BSL", 0b00011, [reg_a, reg_b, reg_save], 4)
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_save = reg_save

    def printInfo(self):
        print(f"    {self.reg_save.getInfo()} = {self.reg_a.getInfo()} << {self.reg_b.getInfo()}")


class BsrInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("BSR", 0b00100, [reg_a, reg_b, reg_save], 4)
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_save = reg_save

    def printInfo(self):
        print(f"    {self.reg_save.getInfo()} = {self.reg_a.getInfo()} >> {self.reg_b.getInfo()}")


class OrInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("OR", 0b00101, [reg_a, reg_b, reg_save], 4)
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_save = reg_save

    def printInfo(self):
        print(f"    {self.reg_save.getInfo()} = {self.reg_a.getInfo()} OR {self.reg_b.getInfo()}")


class AndInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("AND", 0b00111, [reg_a, reg_b, reg_save], 4)
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_save = reg_save

    def printInfo(self):
        print(f"    {self.reg_save.getInfo()} = {self.reg_a.getInfo()} AND {self.reg_b.getInfo()}")


class XorInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("XOR", 0b00110, [reg_a, reg_b, reg_save], 4)
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_save = reg_save

    def printInfo(self):
        print(f"    {self.reg_save.getInfo()} = {self.reg_a.getInfo()} XOR {self.reg_b.getInfo()}")


class NotInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("NOT", 0b01000, [reg_a, EmptyByteParameter(), reg_save], 4)
        self.reg_a = reg_a
        self.reg_save = reg_save

    def printInfo(self):
        print(f"    {self.reg_save.getInfo()} = NOT {self.reg_a.getInfo()}")


class XnorInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("XNOR", 0b01001, [reg_a, reg_b, reg_save], 4)
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_save = reg_save

    def printInfo(self):
        print(f"    {self.reg_save.getInfo()} = {self.reg_a.getInfo()} XNOR {self.reg_b.getInfo()}")


class NandInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("NAND", 0b01010, [reg_a, reg_b, reg_save], 4)
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_save = reg_save

    def printInfo(self):
        print(f"    {self.reg_save.getInfo()} = {self.reg_a.getInfo()} NAND {self.reg_b.getInfo()}")


class MemwInstruction(Instruction):
    def __init__(self, reg_addr: RegisterParameter, addr_offset: int, reg_value: RegisterParameter):
        super().__init__("MEMW", 0b01011, [reg_addr, reg_value, Value8Parameter(addr_offset)], 4)
        self.reg_addr = reg_addr
        self.addr_offset = addr_offset
        self.reg_value = reg_value

    def printInfo(self):
        print(f"    [{self.reg_addr.getInfo()} + {self.addr_offset}] = {self.reg_value.getInfo()}")


class MemrInstruction(Instruction):
    def __init__(self, reg_addr: RegisterParameter, addr_offset: int, reg_save: RegisterParameter):
        super().__init__("MEMR", 0b01100, [reg_addr, Value8Parameter(addr_offset), reg_save], 4)
        self.reg_addr = reg_addr
        self.addr_offset = addr_offset
        self.reg_save = reg_save

    def printInfo(self):
        print(f"    {self.reg_save.getInfo()} = [{self.reg_addr.getInfo()} + {self.addr_offset}]")


class ImmediateInstruction(Instruction):
    def __init__(self, reg_save: RegisterParameter, value: int):
        super().__init__("IMM", 0b01101, [reg_save, Value16Parameter(value)], 4)
        self.reg_save = reg_save
        self.value = value

    def printInfo(self):
        print(f"    {self.reg_save.getInfo()} = {self.value}")


class ImmediatePcInstruction(Instruction):
    def __init__(self, reg_save: RegisterParameter, offset: int):
        super().__init__("IMM", 0b01101, [], 4)
        self.reg_save = reg_save
        self.offset = offset

    def printInfo(self):
        print(f"    {self.reg_save.getInfo()} = PC + {self.offset}")

    def toBytes(self, curr_addr: int, labels: dict[str, int]) -> list[int]:
        value = curr_addr + self.offset
        return [self.opcode] + self.reg_save.toBytes() + Value16Parameter(value).toBytes()


class ImmediateLabelInstruction(Instruction):
    def __init__(self, reg_save: RegisterParameter, label_name: str):
        super().__init__("IMM", 0b01101, [], 4)
        self.reg_save = reg_save
        self.label_name = label_name

    def printInfo(self):
        print(f"    {self.reg_save.getInfo()} = label {self.label_name}")

    def toBytes(self, curr_addr: int, labels: dict[str, int]) -> list[int]:
        if self.label_name not in labels.keys():
            raise JaclangSyntaxError(-1, f"Undefined symbol '{self.label_name}'")
        value = labels[self.label_name]
        return [self.opcode] + self.reg_save.toBytes() + Value16Parameter(value).toBytes()


class MovInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_save: RegisterParameter):
        super().__init__("MOV", 0b01110, [reg_a, EmptyByteParameter(), reg_save], 4)
        self.reg_a = reg_a
        self.reg_save = reg_save

    def printInfo(self):
        print(f"    {self.reg_save.getInfo()} = {self.reg_a.getInfo()}")


class CmpInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter, flags: int):
        super().__init__("CMP", 0b01111, [reg_a, reg_b, Value8Parameter(flags)], 4)


class JmpInstruction(Instruction):
    def __init__(self, reg: RegisterParameter):
        super().__init__("JMP", 0b10000, [reg, EmptyByteParameter(), EmptyByteParameter()], 4)


class GpuDrawInstruction(Instruction):
    def __init__(self, reg_a: RegisterParameter, reg_b: RegisterParameter):
        super().__init__("GPU_DRAW", 0b10001, [reg_a, reg_b, EmptyByteParameter()], 4)


class GpuDisplayInstruction(Instruction):
    def __init__(self):
        super().__init__("GPU_DISPLAY", 0b10010, [EmptyByteParameter()], 2)


class PushInstruction(Instruction):
    def __init__(self, reg: RegisterParameter):
        super().__init__("PUSH", 0b10011, [EmptyByteParameter(), reg, EmptyByteParameter()], 4)


class PopInstruction(Instruction):
    def __init__(self, reg: RegisterParameter):
        super().__init__("POP", 0b10100, [EmptyByteParameter(), EmptyByteParameter(), reg], 4)


class SetSpInstruction(Instruction):
    def __init__(self, reg: RegisterParameter):
        super().__init__("SETSP", 0b10101, [reg], 2)
        self.reg = reg

    def printInfo(self):
        print(f"    SP = {self.reg.getInfo()}")


class GetSpInstruction(Instruction):
    def __init__(self, reg: RegisterParameter):
        super().__init__("GETSP", 0b10110, [EmptyByteParameter(), EmptyByteParameter(), reg], 4)
        self.reg = reg

    def printInfo(self):
        print(f"    {self.reg.getInfo()} = SP")


class LabelInstruction(Instruction):
    def __init__(self, label_name: str):
        super().__init__("", 0b00000, [], 0)
        self.label_name = label_name

    def printInfo(self):
        print(f"{self.label_name}:")

    def preCompile(self, curr_addr: int, labels: dict[str, int]):
        labels[self.label_name] = curr_addr
