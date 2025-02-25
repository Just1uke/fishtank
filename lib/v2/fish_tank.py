import pygame
import random
from .beta_fish import BetaFish
from .puffer_fish import PufferFish
from .stingray import Stingray

class FishTank:
    def __init__(self, width: int, height: int, fps: int):
        pygame.init()
        self.width = width
        self.height = height
        self.fps = fps
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Fish Tank Simulator")
        self.clock = pygame.time.Clock()
        self.running = True

        self.creatures = []  # List to hold all aquatic creatures
        self.initialize_creatures()

    def initialize_creatures(self):
        """Populates the fish tank with creatures."""
        for i in range(3):
            self.creatures.append(
                BetaFish(self, f"Betta {i}", x=random.randint(0, self.width), y=random.randint(0, self.height)))

        for i in range(3):
            self.creatures.append(
                PufferFish(self, f"Puffer {i}", x=random.randint(0, self.width), y=random.randint(0, self.height)))

        for i in range(3):
            self.creatures.append(
                Stingray(self, f"Puffer {i}", x=random.randint(0, self.width), y=random.randint(0, self.height)))

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """Update game state."""
        for creature in self.creatures:
            creature.update()

    def render(self):
        """Render everything to the screen."""
        self.screen.fill((0, 0, 255))  # Blue background for water
        for creature in self.creatures:
            creature.render()
        pygame.display.flip()
