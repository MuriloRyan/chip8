import pygame

PALETTES = {
    "matrix": {"bg": (0, 0, 0), "pixel": (0, 255, 65)},
    "gameboy": {"bg": (155, 188, 15), "pixel": (15, 56, 15)},
    "dracula": {"bg": (40, 42, 54), "pixel": (80, 250, 123)}
}

STANDARD_SETTINGS = {
    "width": 64,
    "height": 32,
    "scale": 15,
    "bg_color": PALETTES["matrix"]["bg"],
    "pixel_color": PALETTES["matrix"]["pixel"],
    "show_debug": False,
    "cycles_per_frame": 10,
    "key_map": {
            pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3, pygame.K_4: 0xC,
            pygame.K_q: 0x4, pygame.K_w: 0x5, pygame.K_e: 0x6, pygame.K_r: 0xD,
            pygame.K_a: 0x7, pygame.K_s: 0x8, pygame.K_d: 0x9, pygame.K_f: 0xE,
            pygame.K_z: 0xA, pygame.K_x: 0x0, pygame.K_c: 0xB, pygame.K_v: 0xF
        }
}