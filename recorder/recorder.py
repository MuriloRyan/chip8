try:
    from mychip8.chip8 import Chip8Hardware
    from mychipssem.assembler import Chip8Assembler
except Exception:
    # Allow running this file directly from the `repl/` folder by adding
    # the project root to `sys.path` at runtime. Prefer running with
    # `python -m repl.repl` from the project root or setting PYTHONPATH.
    import sys
    from pathlib import Path

    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from mychip8.chip8 import Chip8Hardware
    from mychipssem.assembler import Chip8Assembler

class Recorder:
    def __init__(self, machine: Chip8Hardware, assembler= Chip8Assembler):
        self.recording: list = []
        self.machine = machine
        self.assembler = assembler()
        self.number_o_lines = 0
        self.write_ptr = 0x200

    def record(self, opcode: int, page:int = 0, line: int = 0):
        self.recording.append(opcode)
        return opcode
    
    def clear_recording(self):
        self.recording.clear()
        self.write_ptr = 0x200

    def write_memory(self, opcode: bytes):
        opcode_int = int.from_bytes(opcode, 'big')

        hi = (opcode_int >> 8) & 0xFF
        lo = opcode_int & 0xFF

        self.machine.memory[self.write_ptr] = hi
        self.machine.memory[self.write_ptr + 1] = lo

        self.write_ptr += 2

        return opcode_int

    def read_memory(self, addr: int):
        return self.machine.memory[addr]

    def dump_recording(self):
        if not self.recording:
            return "Recording is empty."

        lines = []

        addr = 0x200

        for opcode_bytes in self.recording:
            opcode = int.from_bytes(opcode_bytes, 'big')

            lines.append(
                f"{addr:04X}: {opcode:04X}"
            )

            addr += 2

        return "\n".join(lines)

    def recording_step(self, assembly_entry: str, autoexec=True):
        opcode_bytes = self.assembler.one_step_from_code(assembly_entry)

        if not opcode_bytes:
            return 'invalid assembly code'

        if autoexec:
            self.write_memory(opcode_bytes)
        
        self.record(opcode_bytes)
        self.number_o_lines += 1
        return f'{assembly_entry} saved to recording'
    
    def write_bin_file(self, output_filename: str):
        with open(output_filename, 'wb') as output_file:
            for byte in self.recording:
                output_file.write(byte)
        
        return f'File writen with {self.number_o_lines} lines!'
    
