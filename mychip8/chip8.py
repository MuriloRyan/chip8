from random import randrange

class Chip8Hardware:
    def __init__(self):
        LARGURA, ALTURA = 64, 32
        ESCALA = 10

        self.screen = [[0 for _ in range(LARGURA)] for _ in range(ALTURA)]

        self.memory = [0] * 4096      # RAM
        self.v = [0] * 16             # Registers V0-VF
        self.i = 0                    # index
        self.pc = 0x200               # Program Counter starts at 0x200
        self.stack = [0] * 16         # Stack
        self.sp = 0                   # Stack Pointer
        
        self.delay_timer = 0
        self.sound_timer = 0

    def read_opcode(self, opcode):
        instruction_type = (opcode & 0xF000) >> 12

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
