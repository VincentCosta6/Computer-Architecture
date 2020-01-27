"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self, register_count = 8, calloc_size = 10000):
        """Construct a new CPU."""
        self.reg = [0b00000000] * register_count
        self.ram = [0b00000000] * calloc_size
        self.instruction = 0
        self.active = False

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, position):
        return self.ram[position]

    def ram_write(self, position, binary_value):
        if position < 0 or position >= len(self.ram):
            print("SEG FAULT NO POS")
            sys.exit(1)

        self.ram[position] = binary_value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.instruction,
            #self.fl,
            #self.ie,
            self.ram_read(self.instruction),
            self.ram_read(self.instruction + 1),
            self.ram_read(self.instruction + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self, instruction_start = 0, legacy = False):
        """Run the CPU."""
        self.active = True

        if legacy is True:
            self.run_legacy(instruction_start)
        else:
            self.run_hot(instruction_start)

    def run_legacy(self, instruction_start = 0):
        self.instruction = instruction_start
        self.active = True

        while self.active:
            instruc_val = self.ram[self.instruction]

            if instruc_val == 0b00000001: # HLT: HALT
                # self.trace()
                self.active = False
            elif instruc_val == 0b01000111: # PRN (R#): Print register value
                register = self.ram[self.instruction + 1]

                print(self.reg[register])

                self.instruction += 2
            elif instruc_val == 0b10000010: # LDI (R#, VAL): Load immediate register with value
                register = self.ram[self.instruction + 1]
                value = self.ram[self.instruction + 2]

                if register < 0 or register >= len(self.reg):
                    # self.trace()
                    print("SEG FAULT NO REG")
                    sys.exit(1)

                self.reg[register] = value

                self.instruction += 3

        print("HLT")

    def run_hot(self, instruction_start = 0):
        self.instruction = instruction_start
        self.active = True

        def HLT():
            self.trace()
            self.active = False

        def PRN():
            register = self.ram[self.instruction + 1]

            print(self.reg[register])

            self.instruction += 2

        def LDI():
            register = self.ram[self.instruction + 1]
            value = self.ram[self.instruction + 2]

            if register < 0 or register >= len(self.reg):
                self.trace()
                print("SEG FAULT NO REG")
                sys.exit(1)

            self.reg[register] = value

            self.instruction += 3

        instruction_map = {
            0b00000001: HLT,
            0b01000111: PRN,
            0b10000010: LDI
        }

        while self.active:
            instruction_val = self.ram[self.instruction]

            instruction_map[instruction_val]()

        print("HLT")