import os
from tkinter import *
from tkinter import messagebox

from mychip8.settings import STANDARD_SETTINGS
from mychip8.chip8 import Chip8Hardware
from mychip8.screen import EmulatorScreen


class TestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CHIP-8 Test Runner")
        self.root.geometry("400x400")

        Label(
            root,
            text="CHIP-8 Test Runner",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        BASE = os.path.join(os.path.dirname(__file__), "test_roms")

        self.tests = {
            "CHIP-8 Logo": os.path.join(BASE, "1-chip8-logo.ch8"),
            "IBM Logo": os.path.join(BASE, "2-ibm-logo.ch8"),
            "Corax+": os.path.join(BASE, "3-corax+.ch8"),
            "Flags": os.path.join(BASE, "4-flags.ch8"),
            "Quirks": os.path.join(BASE, "5-quirks.ch8"),
            }

        for name in self.tests:
            frame = Frame(root)
            frame.pack(fill=X, padx=10, pady=5)

            Label(frame, text=name, width=22, anchor=W).pack(side=LEFT)

            Button(
                frame,
                text="Run",
                width=10,
                bg="#4CAF50",
                fg="white",
                command=lambda n=name: self.run_test(n)
            ).pack(side=LEFT)

    def run_test(self, test_name):
        rom = self.tests[test_name]

        if rom is None:
            messagebox.showinfo(
                "Não configurado",
                f"{test_name} ainda não possui ROM."
            )
            return

        if not os.path.exists(rom):
            messagebox.showerror(
                "Erro",
                f"ROM não encontrada:\n{rom}"
            )
            return

        hardware = Chip8Hardware()

        settings = STANDARD_SETTINGS.copy()

        app = EmulatorScreen(hardware, **settings)
        app.init()
        app.loop(hardware, rom)


if __name__ == "__main__":
    root = Tk()
    TestGUI(root)
    root.mainloop()