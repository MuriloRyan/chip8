from calendar import c
from settings import STANDARD_SETTINGS
from screen import EmulatorScreen
from chip8 import Chip8Hardware

def cli_loop():
    user_config = STANDARD_SETTINGS.copy()

    print("\nMyChip8 Emulator CLI")
    print("Murilo R.B Silva - 2026\n")

    print('\ncommands you can use: run, pallettes, exit\n')

    command = input("Enter command (type 'exit' to quit): ")

    if command == 'run':
        rom_path = input("Enter ROM path: ")
        run_emulator(rom_path, user_config)
        return True

    if command == "exit":
        print("Exiting emulator.")
        return False

    elif command == 'pallettes':
        print('Available palettes: matrix, gameboy, dracula')

        choicen = input("Choose a palette: ")
        if choicen in ["matrix", "gameboy", "dracula"]:
            from settings import PALETTES

            user_config["bg_color"] = PALETTES[choicen]["bg"]
            user_config["pixel_color"] = PALETTES[choicen]["pixel"]
            
            print(f"Palette set to {choicen}.")

        else:
            print("Invalid palette choice.")
            print('Available palettes: matrix, gameboy, dracula')

        cli_loop()

    print(f"Command '{command}' not recognized.")
    cli_loop()

def run_emulator(rom_path, settings):
    # 1. Instancia o hardware
    hardware = Chip8Hardware()
    
    # 2. Instancia a tela passando as configurações desempacotadas
    # O ** pega as chaves do dicionário e joga como argumentos nomeados
    app = EmulatorScreen(hardware, **settings)
    
    # 3. Inicializa o pygame e entra no loop
    app.init()
    if not app.loop(hardware, rom_path):
        return False

if __name__ == "__main__":
    cli_loop()