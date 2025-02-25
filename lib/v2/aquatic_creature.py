from typing import Optional
import pygame
# from lib.v2.fish_tank import FishTank
import random
import math

from enum import Enum

from pygame import Vector2


class Sexes(Enum):
    MALE = "Male"
    FEMALE = "Female"


class AquaticCreature:
    def __init__(self, tank: "FishTank", name: str, x: Optional[int] = None, y: Optional[int] = None,
                 mass: float = 1.0):
        self.tank = tank
        self.name = name

        self._sex = None

        self.x = x if x is not None else random.randint(0, tank.width)
        self.y = y if y is not None else random.randint(0, tank.height)

        self.speed = random.uniform(0.5, 2.0)  # Random movement speed
        self.dx, self.dy = self.random_velocity()

    def random_velocity(self) -> Vector2:
        """Generates a random direction for movement."""
        angle = random.uniform(0, 2 * 3.14159)  # Random angle in radians
        return self.speed * pygame.math.Vector2(1, 0).rotate_rad(angle)

    def update(self):
        pass

    def render(self):
        """Render the creature (to be overridden by subclasses)."""
        pass

    @property
    def sex(self):
        if self._sex is None:
            self._sex = random.choice([Sexes.MALE, Sexes.FEMALE])
        return self._sex

    import math
