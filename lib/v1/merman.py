import random
from lib.v1.merperson import Merperson


class Merman(Merperson):
    """Mermen swim smoothly and move toward food deliberately."""

    # NORMAL_EMOJIS = ["🧜‍♂️"]
    # RARE_EMOJIS = ["🧚‍♂️"]  # Fairy Merman

    def __init__(self, name: str, bowl: "Bowl", x: int | None = None, y: int | None = None) -> None:
        emoji = random.choice(self.RARE_EMOJIS) if random.random() < 0.1 else self.NORMAL_EMOJIS[0]
        super().__init__(name=name, bowl=bowl, emoji=emoji, x=x, y=y)
        self.sex = "Male"

    def swim(self, max_x: int, max_y: int) -> None:
        """Mermen move toward food slowly but steadily."""
        super().swim(max_x, max_y)

        if random.random() < 0.5:
            self.x += random.choice([-1, 1])  # Move left or right

        # Keep within bounds
        self.x = max(0, min(self.x, max_x - self.width))
        self.y = max(1, min(self.y, max_y - 2))
