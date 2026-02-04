import pygame

class EmulatorScreen:
    def __init__(self, chip8hardware,width: int, height: int, scale: int,
                 bg_color: tuple, pixel_color: tuple,
                 show_debug: bool, cycles_per_frame: int, key_map: dict):
        
        self.chip8 = chip8hardware
        self.width = width
        self.height = height
        self.scale = scale
        self.bg_color = bg_color
        self.pixel_color = pixel_color
        self.show_debug = show_debug
        self.cycles_per_frame = cycles_per_frame
        self.key_map = key_map

        self.running = False

    def init(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.width * self.scale, self.height * self.scale))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 15)

        pygame.display.set_caption("MyPyChip8")

        self.running = True

    def clear(self):
        self.screen.fill(self.bg_color)
    
    def draw_debug_overlay(self):
        overlay = pygame.Surface((200, self.height * self.scale), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))

        y_offset = 10
        for i in range(16):
            text = self.font.render(f"V{i:X}: {self.chip8.v[i]:02X}", True, (255, 255, 255))
            overlay.blit(text, (10, y_offset))
            y_offset += 20
        
        text_i = self.font.render(f"I:  {self.chip8.i:03X}", True, (255, 255, 0))
        text_pc = self.font.render(f"PC: {self.chip8.pc:03X}", True, (0, 255, 255))
        overlay.blit(text_i, (10, y_offset + 10))
        overlay.blit(text_pc, (10, y_offset + 30))

        self.screen.blit(overlay, (0, 0))
        
    def render(self):
        self.clear()

        for y in range(32):
            for x in range(64):
                if self.chip8.screen[y][x]: # Só desenha se for 1
                    pygame.draw.rect(self.screen, self.pixel_color, 
                                    (x * self.scale, y * self.scale, self.scale, self.scale))
        
        if self.show_debug:
            self.draw_debug_overlay()
    
    def load_rom(self, filename):
        with open(filename, "rb") as f:
            rom_data = f.read()
            for i in range(len(rom_data)):
                self.chip8.memory[0x200 + i] = rom_data[i]
    
    def loop(self, hardware, rom_path):
        self.load_rom(rom_path)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key in self.key_map:
                        hardware.keys[self.key_map[event.key]] = 1
                    
                    if event.key == pygame.K_TAB:
                        self.show_debug = not self.show_debug

                if event.type == pygame.KEYUP:
                    if event.key in self.key_map:
                        hardware.keys[self.key_map[event.key]] = 0

            for _ in range(self.cycles_per_frame):
                self.chip8.cycle()

            if self.chip8.delay_timer > 0:
                self.chip8.delay_timer -= 1
            if self.chip8.sound_timer > 0:
                self.chip8.sound_timer -= 1

            # Rendering logic would go here
            self.render()

            pygame.display.flip()
            self.clock.tick(60)