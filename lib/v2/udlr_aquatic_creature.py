import pygame
from lib.v2.aquatic_creature import AquaticCreature
from typing import Dict, List, Tuple
import math

class UDLRAquaticCreature(AquaticCreature):
    FRAME_SEQUENCE = [0, 1, 2, 1]  # Cyclic animation pattern

    def __init__(
            self,
            tank,
            name: str,
            x: int = None,
            y: int = None,
            sprite_sheet_path: str = "assets/fish_sprites.png",
            sprite_grid_size: Tuple[int, int] = (12, 8),
            animation_data: Dict[str, Tuple[int, int, int]] = None,
    ):
        """
        Generalized fish class that supports UDLR animations from a sprite sheet.

        :param tank: The FishTank instance.
        :param name: Name of the creature.
        :param x: Initial X position.
        :param y: Initial Y position.
        :param sprite_sheet_path: Path to the sprite sheet.
        :param sprite_grid_size: (Columns, Rows) in the sprite sheet.
        :param animation_data: Dictionary mapping directions to (start_row, start_col, frame_count).
        """
        super().__init__(tank, name, x, y)

        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.cols, self.rows = sprite_grid_size
        self.frame_size = (self.sprite_sheet.get_width() // self.cols, self.sprite_sheet.get_height() // self.rows)

        self.animation_data = animation_data or {
            "down": (4, 0, 3),  # Row 5, starts at col 0, 3 frames
            "left": (5, 0, 3),  # Row 6
            "right": (6, 0, 3),  # Row 7
            "up": (7, 0, 3)  # Row 8
        }
        self.animations = None

        self.reload_animations()

        self.direction = "down"  # Default starting direction
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 200  # Milliseconds per frame

    def reload_animations(self):
        self.animations = self.load_animations()

    def load_animations(self) -> Dict[str, List[pygame.Surface]]:
        """Extracts animation frames from the sprite sheet based on (start_row, start_col, frame_count)."""
        return {
            direction: self.extract_frames(row, col, count)
            for direction, (row, col, count) in self.animation_data.items()
        }

    def extract_frames(self, row: int, start_col: int, frame_count: int) -> List[pygame.Surface]:
        """Extracts a variable number of frames from a given row in the sprite sheet."""
        frames = []
        for i in range(frame_count):
            x, y = (start_col + i) * self.frame_size[0], row * self.frame_size[1]
            frame = self.sprite_sheet.subsurface(pygame.Rect(x, y, *self.frame_size))
            frames.append(frame)
        return frames

    def update(self):
        """Handles movement and direction updates."""
        self.x += self.dx
        self.y += self.dy

        creature_width, creature_height = self.frame_size

        # Keep within horizontal bounds
        if self.x < 0:
            self.x = 0
            self.dx = abs(self.dx)  # Move right

        elif self.x > self.tank.width - creature_width:
            self.x = self.tank.width - creature_width
            self.dx = -abs(self.dx)  # Move left

        # Keep within vertical bounds
        if self.y < 0:
            self.y = 0
            self.dy = abs(self.dy)  # Move down

        elif self.y > self.tank.height - creature_height:
            self.y = self.tank.height - creature_height
            self.dy = -abs(self.dy)  # Move up

        self.update_direction()


        # Handle animation timing
        self.animation_timer += self.tank.clock.get_time()
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.direction])

    def update_direction(self):
        """Updates the facing direction based on movement."""
        if abs(self.dx) > abs(self.dy):  # Prioritize horizontal movement
            self.direction = "right" if self.dx > 0 else "left"
        else:
            self.direction = "down" if self.dy > 0 else "up"

    def render(self):
        """Draws the creature using the appropriate animation frame."""
        current_frame = self.animations[self.direction][self.frame_index]
        self.tank.screen.blit(current_frame, (self.x, self.y))

    def apply_boundaries(self):
        """Prevents the creature from leaving the fish tank."""
        creature_width, creature_height = self.frame_size

        # Left & right boundaries
        if self.x < 0:
            self.x = 0
            self.dx = abs(self.dx)  # Move right
        elif self.x > self.tank.width - creature_width:
            self.x = self.tank.width - creature_width
            self.dx = -abs(self.dx)  # Move left

        # Top & bottom boundaries
        if self.y < 0:
            self.y = 0
            self.dy = abs(self.dy)  # Move down
        elif self.y > self.tank.height - creature_height:
            self.y = self.tank.height - creature_height
            self.dy = -abs(self.dy)  # Move up

