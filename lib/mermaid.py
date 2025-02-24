import random
from lib.merperson import Merperson


class Mermaid(Merperson):
    """Mermaids swim playfully and move unpredictably."""

    # NORMAL_EMOJIS = ["🧜‍♀️"]
    # RARE_EMOJIS = ["🧚‍♀️"]  # Fairy Mermaid

    def __init__(self, name: str, bowl: "Bowl", x: int | None = None, y: int | None = None) -> None:
        emoji = random.choice(self.RARE_EMOJIS) if random.random() < 0.1 else self.NORMAL_EMOJIS[0]
        super().__init__(name=name, bowl=bowl, emoji=emoji, x=x, y=y)
        self.sex = "Female"

    def swim(self, max_x: int, max_y: int) -> None:
        """Mermaids are more playful and move unpredictably."""
        super().swim(max_x, max_y)

        if random.random() < 0.3:
            self.x += random.choice([-1, 1])  # Move left or right randomly

        if random.random() < 0.3:
            self.y += random.choice([-1, 1])  # Move up or down randomly

        # Keep within bounds
        self.x = max(0, min(self.x, max_x - self.width))
        self.y = max(1, min(self.y, max_y - 2))
