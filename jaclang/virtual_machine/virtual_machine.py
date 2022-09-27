class VirtualMachine:
    def __init__(self, memory_size: int):
        self.memory = [0] * memory_size
        self.registers = [0] * 8
        self.stack_pointer = 0
        self.program_counter = 0

    def getMemorySize(self):
        return len(self.memory)

    def run(self, instructions: list[int]):
        for i in range(len(instructions)):
            self.memory[i] = instructions[i]
        self.stack_pointer = len(instructions)

        while True:
            curr_opcode = self.memory[self.program_counter]
            if curr_opcode == 0b00000:  # nop
                break
            elif curr_opcode == 0b00001:  # add
                reg_a = self.memory[self.program_counter + 1]
                reg_b = self.memory[self.program_counter + 2]
                reg_save = self.memory[self.program_counter + 3]
                self.registers[reg_save] = self.registers[reg_a] + self.registers[reg_b]
                self.program_counter += 4
            elif curr_opcode == 0b00010:  # sub
                reg_a = self.memory[self.program_counter + 1]
                reg_b = self.memory[self.program_counter + 2]
                reg_save = self.memory[self.program_counter + 3]
                self.registers[reg_save] = self.registers[reg_a] - self.registers[reg_b]
                self.program_counter += 4
            # elif curr_opcode == 0b00011:  # bsl
            #     self.program_counter += 2
            # elif curr_opcode == 0b00100:  # bsr
            #     self.program_counter += 2
            # elif curr_opcode == 0b00101:  # or
            #     self.program_counter += 2
            # elif curr_opcode == 0b00110:  # xor
            #     self.program_counter += 2
            # elif curr_opcode == 0b00111:  # and
            #     self.program_counter += 2
            # elif curr_opcode == 0b01000:  # not
            #     self.program_counter += 2
            # elif curr_opcode == 0b01001:  # xnor
            #     self.program_counter += 2
            # elif curr_opcode == 0b01010:  # nand
            #     self.program_counter += 2
            elif curr_opcode == 0b01011:  # memw
                reg_addr = self.memory[self.program_counter + 1]
                reg_value = self.memory[self.program_counter + 2]
                offset = self.memory[self.program_counter + 3]
                address = self.registers[reg_addr] + offset
                value = self.memory[address * 2] + (self.memory[address * 2 + 1] << 8)
                self.registers[reg_value] = value
                self.program_counter += 4
            # elif curr_opcode == 0b01100:  # memr
            #     self.program_counter += 2
            elif curr_opcode == 0b01101:  # imm
                reg = self.memory[self.program_counter + 1]
                value = self.memory[self.program_counter + 2] + (self.memory[self.program_counter + 3] << 8)
                self.registers[reg] = value
                self.program_counter += 4
            elif curr_opcode == 0b01110:  # mov
                reg = self.memory[self.program_counter + 1]
                reg_save = self.memory[self.program_counter + 3]
                self.registers[reg_save] = self.registers[reg]
                self.program_counter += 4
            # elif curr_opcode == 0b01111:  # jmp
            #     self.program_counter += 2
            # elif curr_opcode == 0b10001:  # gpudraw
            #     self.program_counter += 2
            # elif curr_opcode == 0b10010:  # gpudisplay
            #     self.program_counter += 2
            elif curr_opcode == 0b10011:  # push
                reg = self.memory[self.program_counter + 2]
                self.memory[self.stack_pointer] = self.registers[reg] & 0xFF
                self.memory[self.stack_pointer + 1] = (self.registers[reg] >> 8) & 0xFF
                self.stack_pointer += 2
                self.program_counter += 4
            elif curr_opcode == 0b10100:  # pop
                reg = self.memory[self.program_counter + 3]
                self.stack_pointer -= 2
                self.registers[reg] = self.memory[self.stack_pointer] + (self.memory[self.stack_pointer + 1] << 8)
                self.program_counter += 4
            # elif curr_opcode == 0b10101:  # setsp
            #     self.program_counter += 2
            elif curr_opcode == 0b10110:  # getsp
                reg = self.memory[self.program_counter + 3]
                self.registers[reg] = self.stack_pointer
                self.program_counter += 4
            # elif curr_opcode == 0b10111:  # getpc
            #     self.program_counter += 2
            # elif curr_opcode == 0b11000:  # pusha
            #     self.program_counter += 2
            # elif curr_opcode == 0b11001:  # popa
            #     self.program_counter += 2
            # elif curr_opcode == 0b11010:  # call
            #     self.program_counter += 2
            elif curr_opcode == 0b11011:  # ret
                # todo: implement
                self.program_counter += 2
            else:
                print(f"Unknown opcode: {curr_opcode} {curr_opcode:b}")
                return

        print("Registers:")
        for i in range(8):
            print(f"REG{i}: {self.registers[i]}")

        
