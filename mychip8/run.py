import pygame
from chip8 import Chip8Hardware
from emulator import load_rom, cicle

# Configurações de exibição
SCALE = 15
WIDTH, HEIGHT = 64 * SCALE, 32 * SCALE
BG_COLOR = (20, 20, 20)
PIXEL_COLOR = (0, 255, 65)


# Mapeamento padrão: 
# Teclado PC -> Teclado CHIP-8
KEY_MAP = {
    pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3, pygame.K_4: 0xC,
    pygame.K_q: 0x4, pygame.K_w: 0x5, pygame.K_e: 0x6, pygame.K_r: 0xD,
    pygame.K_a: 0x7, pygame.K_s: 0x8, pygame.K_d: 0x9, pygame.K_f: 0xE,
    pygame.K_z: 0xA, pygame.K_x: 0x0, pygame.K_c: 0xB, pygame.K_v: 0xF
}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MyPyChip8")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 15)

hardware = Chip8Hardware()
load_rom(hardware, 'snake.ch8')

running = True
show_debug = False

def draw_debug_overlay(screen, hardware):
    overlay = pygame.Surface((200, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))

    y_offset = 10
    for i in range(16):
        text = font.render(f"V{i:X}: {hardware.v[i]:02X}", True, (255, 255, 255))
        overlay.blit(text, (10, y_offset))
        y_offset += 20
    
    text_i = font.render(f"I:  {hardware.i:03X}", True, (255, 255, 0))
    text_pc = font.render(f"PC: {hardware.pc:03X}", True, (0, 255, 255))
    overlay.blit(text_i, (10, y_offset + 10))
    overlay.blit(text_pc, (10, y_offset + 30))

    screen.blit(overlay, (0, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.KEYDOWN:
            if event.key in KEY_MAP:
                hardware.keys[KEY_MAP[event.key]] = 1
            
            if event.key == pygame.K_TAB:
                show_debug = not show_debug

        if event.type == pygame.KEYUP:
            if event.key in KEY_MAP:
                hardware.keys[KEY_MAP[event.key]] = 0

    for _ in range(10):
        cicle(hardware)

    if hardware.delay_timer > 0:
        hardware.delay_timer -= 1
    if hardware.sound_timer > 0:
        hardware.sound_timer -= 1

    # 3. Rendering
    screen.fill(BG_COLOR)
    for y in range(32):
        for x in range(64):
            if hardware.screen[y][x]: # Só desenha se for 1
                pygame.draw.rect(screen, PIXEL_COLOR, 
                                (x * SCALE, y * SCALE, SCALE, SCALE))
    
    if show_debug:
        draw_debug_overlay(screen, hardware)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()