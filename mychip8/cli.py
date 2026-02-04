from settings import STANDARD_SETTINGS
from screen import EmulatorScreen
from chip8 import Chip8Hardware

def run_emulator():
    # 1. Instancia o hardware
    hardware = Chip8Hardware()
    
    # 2. Instancia a tela passando as configurações desempacotadas
    # O ** pega as chaves do dicionário e joga como argumentos nomeados
    app = EmulatorScreen(hardware, **STANDARD_SETTINGS)
    
    # 3. Inicializa o pygame e entra no loop
    app.init()
    app.loop(hardware, "snake.ch8")

if __name__ == "__main__":
    run_emulator()