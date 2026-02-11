import os
from tkinter import *
from tkinter import filedialog, messagebox

# Importing your logic
from mychip8.settings import STANDARD_SETTINGS, PALETTES
from mychip8.chip8 import Chip8Hardware
from mychip8.screen import EmulatorScreen

# 1. Initial Configurations
root = Tk()
root.title("Chip8 Launcher")
root.geometry("450x400")

# Variables to store choices
rom_path = StringVar(value="No ROM selected...")
selected_palette = StringVar(value="matrix")
selected_cycles = IntVar(value=10) # Default to 10 cycles

# 2. Action Functions
def select_file():
    file = filedialog.askopenfilename(filetypes=[("CHIP-8 ROM", "*.ch8")])
    if file:
        rom_path.set(file)

def start_emulator():
    path = rom_path.get()
    if not os.path.exists(path):
        messagebox.showerror("Error", "Please select a valid .ch8 file!")
        return

    # Prepare settings dictionary
    colors = PALETTES[selected_palette.get()]
    settings = STANDARD_SETTINGS.copy()
    settings.update({
        "bg_color": colors["bg"],
        "pixel_color": colors["pixel"],
        "cycles_per_frame": selected_cycles.get(),
        "width": 64,
        "height": 32
    })

    root.withdraw() # Hide launcher
    
    # Run Emulator
    hardware = Chip8Hardware()
    app = EmulatorScreen(hardware, **settings)
    app.init()
    app.loop(hardware, path)
    
    root.deiconify() # Show launcher again after closing the game

# 3. Simple Layout (English)
Label(root, text="Chip8 Settings", font=("Arial", 12, "bold")).pack(pady=10)

# ROM Selection
Label(root, textvariable=rom_path, fg="blue", wraplength=300).pack()
Button(root, text="Browse ROM", command=select_file).pack(pady=5)

# Palette Selection
Label(root, text="Select Palette:").pack(pady=(10, 0))
palette_menu = OptionMenu(root, selected_palette, *PALETTES.keys())
palette_menu.pack()

# Cycles Selection (Speed)
Label(root, text="Cycles per Frame (Speed):").pack(pady=(10, 0))
cycles_menu = OptionMenu(root, selected_cycles, 10, 20)
cycles_menu.pack()

# Play Button
Button(root, text="RUN EMULATOR", bg="green", fg="white", 
       command=start_emulator, font=("Arial", 10, "bold")).pack(pady=20)

root.mainloop()