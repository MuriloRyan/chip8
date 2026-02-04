from random import randrange
from mychip8.opcodes import OPCODE_TABLE, SUB_TABLE_0, SUB_TABLE_8, SUB_TABLE_E, SUB_TABLE_F

class Chip8Hardware:
    def __init__(self, opcode_table = OPCODE_TABLE, opcode_table0 = SUB_TABLE_0,
                 opcode_table8 = SUB_TABLE_8, opcode_tableE = SUB_TABLE_E,
                 opcode_tableF = SUB_TABLE_F):
        LARGURA, ALTURA = 64, 32

        self.screen = [[0 for _ in range(LARGURA)] for _ in range(ALTURA)]

        self.opcode_table = opcode_table
        self.opcode_table0 = opcode_table0
        self.opcode_table8 = opcode_table8
        self.opcode_tableE = opcode_tableE
        self.opcode_tableF = opcode_tableF

        self.memory = [0] * 4096      # RAM
        self.v = [0] * 16             # Registers V0-VF
        self.i = 0                    # index
        self.pc = 0x200               # Program Counter starts at 0x200
        self.stack = [0] * 16         # Stack
        self.sp = 0                   # Stack Pointer

        self.keys = [0] * 16
        self.waiting_key = 0

        self.delay_timer = 0
        self.sound_timer = 0
    
        self.fontset = [
            0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
            0x20, 0x60, 0x20, 0x20, 0x70, # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
            0x90, 0x90, 0xF0, 0x10, 0x10, # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
            0xF0, 0x10, 0x20, 0x40, 0x40, # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90, # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
            0xF0, 0x80, 0x80, 0x80, 0xF0, # C
            0xE0, 0x90, 0x90, 0x90, 0xE0, # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
            0xF0, 0x80, 0xF0, 0x80, 0x80  # F
        ]
    
        for i, byte in enumerate(self.fontset):
            self.memory[i] = byte

    def cycle(self):
        hi_bytes, lo_bytes = (self.memory[self.pc]), self.memory[self.pc+1]
        opcode = (hi_bytes << 8)| lo_bytes

        self.read_opcode(opcode)
        return f'{hex(opcode)} at {hex(self.pc)}'

    def read_opcode(self, opcode):
        if opcode == 0x0000:
            return opcode

        self.pc += 2

        # Decode
        first = (opcode & 0xF000) >> 12
        
        method_name = self.opcode_table.get(first)
        # Sub-selection logic
        if method_name == "TABLE_0":
            method_name = self.opcode_table0.get(opcode)
            getattr(self, method_name)()
            
            return opcode
        elif method_name == "TABLE_8":
            method_name = self.opcode_table8.get(opcode & 0x000F)
        elif method_name == "TABLE_E":
            method_name = self.opcode_tableE.get(opcode & 0x00FF)
        elif method_name == "TABLE_F":
            method_name = self.opcode_tableF.get(opcode & 0x00FF)

        # Execute
        if method_name:
            method = getattr(self, method_name)
            method(opcode)

            return opcode

    # --- 0x0: SYSTEM INSTRUCTIONS ---
    def CLS(self):
        """00E0: Clear the display (fills the screen matrix with 0)."""
        self.screen = [[0 for _ in range(64)] for _ in range(32)]
    
    def RET(self):
        """00EE: Return from a subroutine. Pops the address from the stack."""
        self.sp -= 1
        self.pc = self.stack[self.sp]
    
    # --- 0x1 & 0x2: JUMP AND CALL ---
    def JUMP(self, opcode):
        """1NNN: Jump to address NNN. Set PC = NNN."""
        nnn = (opcode & 0x0FFF)
        self.pc = nnn
        
    def CALL(self, opcode):
        """2NNN: Call subroutine at NNN. Push PC to stack and jump to NNN."""
        address = (opcode & 0x0FFF)
        self.stack[self.sp] = self.pc
        self.sp += 1
        self.pc = address
    
    # --- 0x3, 0x4, 0x5 & 0x9: CONDITIONAL SKIPS ---
    def SE_Vx_byte(self, opcode):
        """3XKK: Skip next instruction if VX == KK."""
        x = (opcode & 0x0F00) >> 8
        kk = (opcode & 0x00FF)
        if self.v[x] == kk:
            self.pc += 2

    def SNE_Vx_byte(self, opcode):
        """4XKK: Skip next instruction if VX != KK."""
        x = (opcode & 0x0F00) >> 8
        kk = (opcode & 0x00FF)
        if self.v[x] != kk:
            self.pc += 2

    def SE_Vx_Vy(self, opcode):
        """5XY0: Skip next instruction if VX == VY."""
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        if self.v[x] == self.v[y]:
            self.pc += 2

    def SNE_Vx_Vy(self, opcode):
        """9XY0: Skip next instruction if VX != VY."""
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        if self.v[x] != self.v[y]:
            self.pc += 2
    
    # --- 0x6 & 0x7: ASSIGNMENT AND ARITHMETIC ---
    def LD_Vx_byte(self, opcode):
        """6XKK: Set VX = KK."""
        x = (opcode & 0x0F00) >> 8
        kk = (opcode & 0x00FF)
        self.v[x] = kk

    def ADD_Vx_byte(self, opcode):
        """7XKK: Set VX = VX + KK (Does not affect VF)."""
        x = (opcode & 0x0F00) >> 8
        kk = (opcode & 0x00FF)
        self.v[x] = (self.v[x] + kk) & 0xFF

    # --- 0x8: ALU OPERATIONS ---
    def LD_Vx_Vy(self, opcode):
        """8XY0: Set VX = VY."""
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        self.v[x] = self.v[y]

    def OR_Vx_Vy(self, opcode):
        """8XY1: Set VX = VX OR VY."""
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        self.v[x] |= self.v[y]

    def AND_Vx_Vy(self, opcode):
        """8XY2: Set VX = VX AND VY."""
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        self.v[x] &= self.v[y]

    def XOR_Vx_Vy(self, opcode):
        """8XY3: Set VX = VX XOR VY."""
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        self.v[x] ^= self.v[y]

    def ADD_Vx_Vy(self, opcode):
        """8XY4: Set VX = VX + VY. Set VF = 1 if carry (> 255)."""
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        sum_val = self.v[x] + self.v[y]
        self.v[0xF] = 1 if sum_val > 255 else 0
        self.v[x] = sum_val & 0xFF

    def SUB_Vx_Vy(self, opcode):
        """8XY5: Set VX = VX - VY. Set VF = 1 if NOT borrow (VX >= VY)."""
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        self.v[0xF] = 1 if self.v[x] >= self.v[y] else 0
        self.v[x] = (self.v[x] - self.v[y]) & 0xFF

    def SHR_Vx_Vy(self, opcode):
        """8XY6: Set VX = VX SHR 1. VF = Least Significant Bit (LSB)."""
        x = (opcode & 0x0F00) >> 8
        self.v[0xF] = self.v[x] & 0x1
        self.v[x] >>= 1

    def SUBN_Vx_Vy(self, opcode):
        """8XY7: Set VX = VY - VX. Set VF = 1 if NOT borrow (VY >= VX)."""
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        self.v[0xF] = 1 if self.v[y] >= self.v[x] else 0
        self.v[x] = (self.v[y] - self.v[x]) & 0xFF

    def SHL_Vx_Vy(self, opcode):
        """8XYE: Set VX = VX SHL 1. VF = Most Significant Bit (MSB)."""
        x = (opcode & 0x0F00) >> 8
        self.v[0xF] = (self.v[x] & 0x80) >> 7
        self.v[x] = (self.v[x] << 1) & 0xFF
    
    def LD_I(self, opcode):
        """ANNN: Set Index Register I = NNN."""
        nnn = (opcode & 0x0FFF)
        self.i = nnn
    
    def JUMP_V0(self, opcode):
        """BNNN: Jump to location NNN + V0."""
        nnn = (opcode & 0x0FFF)
        self.pc = nnn + self.v[0x0]

    def RND_Vx_byte(self, opcode):
        """CXKK: Set VX = (random byte) AND KK."""
        x = (opcode & 0x0F00) >> 8
        kk = (opcode & 0x00FF)
        self.v[x] = randrange(256) & kk

    def DRW_Vx_Vy_nibble(self, opcode):
        """
        DXYN: Draw a sprite at (VX, VY) with N bytes of height.
        The sprite is stored in memory starting at the location stored in I.
        VF is set to 1 if any screen pixels are flipped from set to unset (collision).
        """

        x_reg = (opcode & 0x0F00) >> 8
        y_reg = (opcode & 0x00F0) >> 4
        height = (opcode & 0x000F)
        x_start = self.v[x_reg] % 64
        y_start = self.v[y_reg] % 32

        self.v[0xF] = 0

        for row in range(height):

            sprite_byte = self.memory[self.i + row]

            for col in range(8):
                sprite_pixel = (sprite_byte >> (7 - col)) & 1

                if sprite_pixel == 1:
                    curr_x = (x_start + col) % 64
                    curr_y = (y_start + row) % 32

                    if self.screen[curr_y][curr_x] == 1:
                        self.v[0xF] = 1

                    self.screen[curr_y][curr_x] ^= 1
    
    def SKP_Vx(self, opcode):
        """ EX9E: Skip next instruction if key with the value of VX is pressed. """
        x = (opcode & 0x0F00) >> 8
        key = self.v[x]
        if self.keys[key] == 1:
            self.pc += 2

    def SKNP_Vx(self, opcode):
        """ EXA1: Skip next instruction if key with the value of VX is NOT pressed. """
        x = (opcode & 0x0F00) >> 8
        key = self.v[x]
        if self.keys[key] == 0:
            self.pc += 2
    
    def LD_Vx_DT(self, opcode):
        """ Fx07 """
        x = (opcode & 0x0F00) >> 8

        self.v[x] = self.delay_timer
    
    def LD_Vx_K(self, opcode):
        """ Fx0A: Wait for key press. VX = index of the key. """
        x = (opcode & 0x0F00) >> 8
        key_detected = False

        for index, is_pressed in enumerate(self.keys):
            if is_pressed == 1:
                self.v[x] = index
                key_detected = True
                break
        if not key_detected:
            self.pc -= 2
            
    def LD_DT_Vx(self, opcode):
        """ Fx15 """
        x = (opcode & 0x0F00) >> 8

        self.delay_timer = self.v[x]

    def LD_ST_Vx(self, opcode):
        """ Fx18 """
        x = (opcode & 0x0F00) >> 8

        self.sound_timer = self.v[x]
    
    def ADD_I_Vx(self, opcode):
        """ Fx1E: Set I = I + VX. """
        x = (opcode & 0x0F00) >> 8
        self.i = (self.i + self.v[x]) & 0xFFF

    def LD_B_Vx(self, opcode):
        """ FX33 """
        x = (opcode & 0x0F00) >> 8

        number = self.v[x]

        self.memory[self.i] = number // 100
        self.memory[self.i + 1] = (number % 100) // 10
        self.memory[self.i + 2] = (number % 10)

    def LD_I_Vx(self, opcode):
        """ FX55 """
        x = (opcode & 0x0F00) >> 8

        for count in range(x + 1):
            self.memory[self.i + count] = self.v[count]

    def LD_Vx_I(self, opcode):
        """ Fx65 """

        x = (opcode & 0x0F00) >> 8

        for count in range(x + 1):
            self.v[count] = self.memory[self.i + count]
    
    def LD_F_Vx(self, opcode):
        """ FX29: Point I to the font sprite for the character in VX. """
        x = (opcode & 0x0F00) >> 8
        character = self.v[x] & 0x0F
        
        self.i = character * 5