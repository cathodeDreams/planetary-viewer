import pygame
from config import Config
from camera import Camera
from planet import Planet
from renderer import Renderer

class PlanetaryViewer:
    def __init__(self, config: Config):
        self.config = config
        self.renderer = Renderer(config)
        self.camera = Camera(config)
        self.planet = Planet(config)
        self.time = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False
            elif event.type == pygame.MOUSEMOTION:
                dx, dy = event.rel
                self.camera.update(dx, dy, 0)  # Pass 0 as dt here, actual dt is passed in run loop
            elif event.type == pygame.MOUSEWHEEL:
                self.camera.zoom(event.y)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.camera.toggle_mode()

        keys = pygame.key.get_pressed()
        if self.camera.mode == 'free':
            forward = keys[pygame.K_w] - keys[pygame.K_s]
            right = keys[pygame.K_d] - keys[pygame.K_a]
            up = keys[pygame.K_e] - keys[pygame.K_q]
            boost = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
            self.camera.move(forward, right, up, boost)

        return True

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            dt = clock.tick(self.config.fps) / 1000.0
            self.time += dt
            running = self.handle_events()
            self.camera.update(0, 0, dt)  # Update camera with delta time
            self.camera.check_collision(self.config.planet_radius)
            self.renderer.render(self.planet, self.camera, self.time)
        pygame.quit()