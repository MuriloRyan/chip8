from chip8 import Chip8Hardware
import pygame

chip8 = Chip8Hardware()
scale = 10

pygame.init()
emulator_screen = pygame.display.set_mode((64 * scale,32 * scale))
pygame.display.set_caption("CHIP-8 Emulator")

def update_screen(screen):
    for y in range(32):
        for x in range(64):
            if screen[y][x] == 1:
                pygame.draw.rect(emulator_screen, (255, 255, 255), 
                                 (x * scale, y * scale, scale, scale))

clock = pygame.time.Clock()

def update_display(matrix, surface, scale_factor):
    surface.fill((0, 0, 0))

    for y in range(32):
        for x in range(64):
            if matrix[y][x] == 1:

                pygame.draw.rect(
                    surface, 
                    (255, 255, 255), 
                    (x * scale_factor, y * scale_factor, scale_factor, scale_factor)
                )

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update_display(chip8.screen, emulator_screen, scale)
    
    pygame.display.flip()

    clock.tick(60)

pygame.quit()