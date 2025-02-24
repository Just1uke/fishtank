import random
from .aquatic_creature import AquaticCreature
from .cookie import Cookie


class Jellyfish(AquaticCreature):
    """Jellyfish float gracefully up and down."""
    NORMAL_EMOJIS = ["🪼"]
    RARE_EMOJIS = ["🦑", "🐙"]

    def __init__(self, name: str, bowl: 'Bowl', x: int | None = None, y: int | None = None) -> None:
        super().__init__(name=name, bowl=bowl, emoji=random.choice(self.NORMAL_EMOJIS), x=x, y=y)

    def swim(self, max_x: int, max_y: int) -> None:
        """Jellyfish primarily move up/down, occasionally drifting sideways."""
        super().swim(max_x=max_x, max_y=max_y)
        if random.random() < 0.3:
            self.y += random.choice([-1, 1])  # Move up or down
        if random.random() < 0.1:
            self.x += random.choice([-1, 1])  # Slight horizontal drift

        # Keep within bounds
        self.x = max(0, min(self.x, max_x - self.width))
        self.y = max(1, min(self.y, max_y - 2))
