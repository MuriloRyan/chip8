"""
Chip8 Opcode Table (Polymorphic Version)
Mnemonic Keys pointing to a list of syntax variants using generic 'reg'.
"""

MNEMONIC_TABLE = {
    "CLS": [
        {"opcode": 0x00E0, "args": []}
    ],
    
    "RET": [
        {"opcode": 0x00EE, "args": []}
    ],
    
    "JP": [
        {"opcode": 0x1000, "args": ["addr"]},
        {"opcode": 0xB000, "args": ["v0", "addr"]}  # JP V0, ADDR
    ],
    
    "CALL": [
        {"opcode": 0x2000, "args": ["addr"]}
    ],
    
    "SE": [
        {"opcode": 0x3000, "args": ["reg", "byte"]},
        {"opcode": 0x5000, "args": ["reg", "reg"]}
    ],
    
    "SNE": [
        {"opcode": 0x4000, "args": ["reg", "byte"]},
        {"opcode": 0x9000, "args": ["reg", "reg"]}
    ],
    
    "LD": [
        {"opcode": 0x6000, "args": ["reg", "byte"]},
        {"opcode": 0x8000, "args": ["reg", "reg"]},
        {"opcode": 0xA000, "args": ["i", "addr"]},    # LD I, ADDR
        {"opcode": 0xF007, "args": ["reg", "dt"]},    # LD VX, DT
        {"opcode": 0xF00A, "args": ["reg", "k"]},     # LD VX, K
        {"opcode": 0xF015, "args": ["dt", "reg"]},    # LD DT, VX
        {"opcode": 0xF018, "args": ["st", "reg"]},    # LD ST, VX
        {"opcode": 0xF029, "args": ["f", "reg"]},     # LD F, VX
        {"opcode": 0xF033, "args": ["b", "reg"]},     # LD B, VX
        {"opcode": 0xF055, "args": ["i", "reg"]},     # LD [I], VX
        {"opcode": 0xF065, "args": ["reg", "i"]}      # LD VX, [I]
    ],
    
    "ADD": [
        {"opcode": 0x7000, "args": ["reg", "byte"]},
        {"opcode": 0x8004, "args": ["reg", "reg"]},
        {"opcode": 0xF01E, "args": ["i", "reg"]}      # ADD I, VX
    ],
    
    "OR": [
        {"opcode": 0x8001, "args": ["reg", "reg"]}
    ],
    
    "AND": [
        {"opcode": 0x8002, "args": ["reg", "reg"]}
    ],
    
    "XOR": [
        {"opcode": 0x8003, "args": ["reg", "reg"]}
    ],
    
    "SUB": [
        {"opcode": 0x8005, "args": ["reg", "reg"]}
    ],
    
    "SUBN": [
        {"opcode": 0x8007, "args": ["reg", "reg"]}
    ],
    
    "SHR": [
        {"opcode": 0x8006, "args": ["reg"]}
    ],
    
    "SHL": [
        {"opcode": 0x800E, "args": ["reg"]}
    ],
    
    "RND": [
        {"opcode": 0xC000, "args": ["reg", "byte"]}
    ],
    
    "DRW": [
        {"opcode": 0xD000, "args": ["reg", "reg", "nibble"]}
    ],
    
    "SKP": [
        {"opcode": 0xE09E, "args": ["reg"]}
    ],
    
    "SKNP": [
        {"opcode": 0xE0A1, "args": ["reg"]}
    ]
}