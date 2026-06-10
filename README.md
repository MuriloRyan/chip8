## MyChip8

screen.py is a test of screen working, not final file

How it works:

    - mychip8/chip8.py:
        its the main file of the project, since its the base for the "hardware" of the VM
    
        Chip8Hardware is a class that handles all chip8 operations,
        such as geting the bytes with .cycle() or execute the opcodes with .read_opcode()

    - mychip8/screen.py:

        EmulatorScreen is a class that handles the execution of chip8 and generates the screen

        it receives an example of Chip8 interpreter in its init ad an argument called "chip8hardware":

        ```python
        class EmulatorScreen:
            def __init__(self, chip8hardware,width: int, height: int, scale: int,
            bg_color: tuple, pixel_color: tuple, show_debug: bool, cycles_per_frame: int, key_map: dict):
        ```