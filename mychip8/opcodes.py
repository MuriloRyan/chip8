# --- OPCODE TABLES ---

# Main table: Key is the first nibble (opcode >> 12)
OPCODE_TABLE = {
    0x0: "TABLE_0",
    0x1: "JUMP",
    0x2: "CALL",
    0x3: "SE_Vx_byte",
    0x4: "SNE_Vx_byte",
    0x5: "SE_Vx_Vy",
    0x6: "LD_Vx_byte",
    0x7: "ADD_Vx_byte",
    0x8: "TABLE_8",
    0x9: "SNE_Vx_Vy",
    0xA: "LD_I",
    0xB: "JUMP_V0",
    0xC: "RND_Vx_byte",
    0xD: "DRW_Vx_Vy_nibble",
    0xE: "TABLE_E",
    0xF: "TABLE_F"
}

# Sub-table for instructions starting with 0x0
SUB_TABLE_0 = {
    0x00E0: "CLS",
    0x00EE: "RET"
}

# Sub-table for ALU operations starting with 0x8 (Key is last nibble)
SUB_TABLE_8 = {
    0x0: "LD_Vx_Vy",
    0x1: "OR_Vx_Vy",
    0x2: "AND_Vx_Vy",
    0x3: "XOR_Vx_Vy",
    0x4: "ADD_Vx_Vy",
    0x5: "SUB_Vx_Vy",
    0x6: "SHR_Vx_Vy",
    0x7: "SUBN_Vx_Vy",
    0xE: "SHL_Vx_Vy"
}

# Sub-table for Input (starting with 0xE)
SUB_TABLE_E = {
    0x9E: "SKP_Vx",
    0xA1: "SKNP_Vx"
}

# Sub-table for Timers, Memory, BCD (starting with 0xF)
SUB_TABLE_F = {
    0x07: "LD_Vx_DT",
    0x0A: "LD_Vx_K",
    0x15: "LD_DT_Vx",
    0x18: "LD_ST_Vx",
    0x1E: "ADD_I_Vx",
    0x29: "LD_F_Vx",   # Point I to character font
    0x33: "LD_B_Vx",   # BCD conversion
    0x55: "LD_I_Vx",   # Store registers in memory (Dump)
    0x65: "LD_Vx_I"    # Load registers from memory (Load)
}