import random
from typing import Optional

from .aquatic_creature import AquaticCreature
from .cookie import Cookie


class Crab(AquaticCreature):
    NORMAL_EMOJIS = ["🦀"]
    RARE_EMOJIS = ["🦞"]
    """Crabs stay near the bottom but chase food."""

    def __init__(self, name: str, bowl: 'Bowl', x: int | None = None, y: int | None = None) -> None:
        super().__init__(name=name, bowl=bowl, emoji=random.choice(self.NORMAL_EMOJIS), x=x, y=bowl.height - 2)

    def update(self) -> None:
        """Crabs only move left or right and always stay at the bottom."""
        super().update()

        # Crabs can only move left/right
        self.y = self.bowl.height - 2  # ✅ Lock crabs to bottom!

    def swim(self, max_x: int, max_y: int) -> None:
        """Crabs only move left or right, and always stay at the bottom."""
        occupied = self.bowl.get_occupied_positions()

        if self.closest_food:
            # ✅ Move toward food horizontally only
            if self.x < self.closest_food.x and (self.x + 1, self.y) not in occupied:
                self.x += 1
            elif self.x > self.closest_food.x and (self.x - 1, self.y) not in occupied:
                self.x -= 1
        else:
            # ✅ Move randomly left or right if no food is present
            new_x = self.x + random.choice([-1, 1])
            if (new_x, self.y) not in occupied and 1 <= new_x < max_x - 1:
                self.x = new_x

        # ✅ Ensure crabs stay at the bottom
        self.y = max_y - 2
