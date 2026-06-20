try:
    from opcode_table import MNEMONIC_TABLE
    from string import hexdigits
except ImportError:
    from mychipssem.opcode_table import MNEMONIC_TABLE
    from string import hexdigits

class Chip8Assembler:

    def __init__(self, opcode_table = MNEMONIC_TABLE) -> None:
        self.labels = {}
        self.scanned = []
        self.resolved = []
        self.encoded = {}
        self.current_addr = 0x200
        self.opcode_table = opcode_table

    def scan(self, line: str) -> list | None:
        if ';' in line:
            line = line.split(';')[0]

        # Clean whitespaces and commas to avoid splitting issues
        line = line.strip().replace(',', ' ')

        if line == "":
            return None

        if line.endswith(':'):
            label = line[:-1].strip()
            self.labels[label] = self.current_addr
            return None

        parts = line.split(maxsplit=1)
        instruction = parts[0].upper() # Normalize mnemonic to uppercase

        if len(parts) > 1:
            arguments = parts[1].strip().split()
        else:
            arguments = []

        self.current_addr += 0x2

        self.scanned.append({
            "instruction": instruction,
            "args": arguments
        })

        return None

    def resolve(self):
        for item in self.scanned:
            instruction = item["instruction"]
            args = item["args"]
            new_args = []

            for arg in args:
                # If an arg is in the labels list, replace it with the address integer
                if arg in self.labels:
                    new_args.append(self.labels[arg])
                else:
                    new_args.append(arg)

            self.resolved.append({
                "instruction": instruction,
                "args": new_args
            })

        return None 

    def check_args(self, instruction, args):
        if instruction not in self.opcode_table:
            raise ValueError(f"Unknown mnemonic: {instruction}")

        user_args_types = []
        
        for arg in args:
            # Convert to string and uppercase for uniform keyword verification
            arg_str = str(arg).upper()

            # Case A: Strict Keyword match for the 'I' register
            if arg_str == 'I':
                user_args_types.append("i")
                
            # Case B: Strict Keyword match for the V0 register
            elif arg_str == 'V0':
                user_args_types.append("v0")
                
            # Case C: Strict Keyword match for Delay Timer, Sound Timer, etc.
            elif arg_str in ["DT", "ST", "K", "F", "B"]:
                user_args_types.append(arg_str.lower())
                
            # Case D: General Register match (V1 to VF)
            elif arg_str.startswith('V') and len(arg_str) == 2 and arg_str[1] in hexdigits:
                user_args_types.append("reg")
                
            # Case E: Numerical values (integers, decimal strings, or 0x hex)
            elif isinstance(arg, int) or arg_str.startswith("0X") or arg_str.isdigit():
                user_args_types.append("numeric")
                
            else:
                raise ValueError(f"Invalid argument syntax: {arg}")

        # 3. Pattern Matching Stage
        variants_list = self.opcode_table[instruction]
        
        for variant in variants_list:
            expected_args = variant["args"]
            
            # Check 1: Arity validation
            if len(expected_args) != len(user_args_types):
                continue  
                
            # Check 2: Structural compatibility alignment
            match_found = True
            
            for expected, user_type in zip(expected_args, user_args_types):
                # General rule for numbers: 'numeric' fits 'byte', 'addr', and 'nibble'
                if expected in ["byte", "addr", "nibble"] and user_type == "numeric":
                    continue  
                    
                # General rule for registers
                elif expected == "reg" and user_type == "reg":
                    continue
                
                # Crucial Fix: V0 can act as a standard general register ("reg") when needed
                elif expected == "reg" and user_type == "v0":
                    continue
                    
                # Strict rule for hardware keywords ('i', 'dt', 'st', etc.)
                elif expected == user_type:
                    continue
                    
                else:
                    match_found = False
                    break
                    
            # 4. Target Selection
            if match_found:
                return variant

        # 5. Fallback Error Handling
        raise TypeError(f"Invalid arguments for instruction '{instruction}': {args}")
    

    def encode(self, instruction: str, args: list):
        # Call check_args to get the correct polymorphic variant dictionary
        variant = self.check_args(instruction, args)

        opcode_base = variant["opcode"]
        expected_args = variant["args"]

        opcode = opcode_base

        # Using enumerate to track the structural position of the arguments
        for index, (arg_type, arg_value) in enumerate(zip(expected_args, args)):

            # -------------------------
            # REGISTER (0-F)
            # -------------------------
            if arg_type == "reg":
                # Strip the 'V' or 'v' prefix and extract hex value
                reg_hex = str(arg_value)[1:]
                reg = int(reg_hex, 16)
                
                # Index 0 means Vx position (0x.X..), Index 1 means Vy position (0x..Y.)
                if index == 0:
                    opcode |= (reg << 8)
                elif index == 1:
                    opcode |= (reg << 4)

            # -------------------------
            # BYTE (0-255 or 0xFF)
            # -------------------------
            elif arg_type == "byte":
                if isinstance(arg_value, str) and str(arg_value).upper().startswith("0X"):
                    value = int(arg_value, 16)
                else:
                    value = int(arg_value)

                opcode |= (value & 0xFF)

            # -------------------------
            # ADDRESS (0x000 - 0xFFF)
            # -------------------------
            elif arg_type == "addr":
                if isinstance(arg_value, str):
                    if arg_value.upper().startswith("0X"):
                        value = int(arg_value, 16)
                    else:
                        value = int(arg_value)
                else:
                    value = arg_value

                opcode |= (value & 0x0FFF)

            # -------------------------
            # NIBBLE (0-15)
            # -------------------------
            elif arg_type == "nibble":
                opcode |= (int(arg_value) & 0xF)

            # -------------------------
            # HARDWARE KEYWORDS (i, dt, st, v0, etc.)
            # -------------------------
            elif arg_type in ["i", "dt", "st", "v0", "k", "f", "b"]:
                # Static keywords do not alter opcode bits directly; they are part of the opcode_base
                continue

            else:
                raise ValueError(f"Unknown arg type: {arg_type}")

        return opcode.to_bytes(2, byteorder="big")

    def one_step_from_code(self, entry: str):
        self.scanned.clear()
        self.resolved.clear()

        self.scan(entry)
        self.resolve()

        instruction = self.resolved[0]

        return self.encode(
            instruction["instruction"],
            instruction["args"]
        )

    def cycle_with_file(self, input_filename: str, output_filename: str):
        with open(input_filename, 'r') as input_file:
            for line in input_file:
                self.scan(line)
        
        self.resolve()
        encoded_bytes = []

        for instruction in self.resolved:
            encoded_bytes.append(self.encode(instruction['instruction'], instruction['args']))

        with open(output_filename, 'wb') as output_file:
            for byte in encoded_bytes:
                output_file.write(byte)


