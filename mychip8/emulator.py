from chip8 import Chip8Hardware

hardware = Chip8Hardware()

def load_rom(hardware, filename):
        """Read ROM file and load it into memory starting at 0x200."""
        with open(filename, "rb") as f:
            rom_data = f.read()
            for i in range(len(rom_data)):
                # Carrega o byte na posição 0x200 + offset
                hardware.memory[0x200 + i] = rom_data[i]
        

def cicle(hardware):
    hi_bytes, lo_bytes = (hardware.memory[hardware.pc]), hardware.memory[hardware.pc+1]
    opcode = (hi_bytes << 8)| lo_bytes

    hardware.read_opcode(opcode)
    return f'{hex(opcode)} - {int(opcode)} - {hex(hardware.pc)}'
