import random
from lib.v1.aquatic_creature import AquaticCreature

class Shrimp(AquaticCreature):
    """Shrimp move in circles rather than randomly."""

    NORMAL_EMOJIS = ["🦐"]
    RARE_EMOJIS = ["🦞"]  # Rare mutation: Lobster Shrimp

    def __init__(self, name: str, bowl: "Bowl", x: int | None = None, y: int | None = None) -> None:
        emoji = random.choice(self.RARE_EMOJIS) if random.random() < 0.1 else self.NORMAL_EMOJIS[0]
        super().__init__(name=name, bowl=bowl, emoji=emoji, x=x, y=y)

        # Define circular movement pattern
        self.circle_pattern = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Right → Down → Left → Up
        self.circle_index = 0  # Start at the first movement in the pattern

    def swim(self, max_x: int, max_y: int) -> None:
        """Shrimp move in circular patterns."""
        super().swim(max_x, max_y)

        # Try to move in the next direction of the circle
        dx, dy = self.circle_pattern[self.circle_index]
        new_x, new_y = self.x + dx, self.y + dy

        # If movement is blocked, try the next step in the pattern
        self.circle_index = (self.circle_index + 1) % len(self.circle_pattern)

        # Keep shrimp within bounds
        if 1 <= new_x < max_x - 1 and 1 <= new_y < max_y - 1:
            self.x, self.y = new_x, new_y
