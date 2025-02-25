import random
from .aquatic_creature import AquaticCreature
from .cookie import Cookie


class Fish(AquaticCreature):
    NORMAL_EMOJIS = ["🐠", "🐟"]
    RARE_EMOJIS = ["🐡"]
    """Standard fish that moves smoothly in all directions."""

    def __init__(self, name: str, bowl: 'Bowl', x: int | None = None, y: int | None = None) -> None:
        super().__init__(name=name, bowl=bowl, emoji=random.choice(self.NORMAL_EMOJIS), x=x, y=y)

    def update(self) -> None:
        """Fish swim normally and inherit base movement from AquaticCreature."""
        super().update()

        # Fish sometimes move randomly
        if random.random() < 0.2:
            self.random_movement()
