import random
import time
from typing import Optional

from lib.aquatic_creature import AquaticCreature


class Merperson(AquaticCreature):
    """Base class for Mermen and Mermaids."""
    RARITY_CHANCE = .05
    NORMAL_EMOJIS = ['🧜']
    RARE_EMOJIS = ['🧜']

    def __init__(self, name: str, bowl: 'Bowl', emoji: str, x: int | None = None, y: int | None = None) -> None:
        super().__init__(name=name, bowl=bowl, emoji=emoji, x=x, y=y)

        self.gender = random.choice([self.sex, "They"])

    def swim(self, max_x: int, max_y: int) -> None:
        """Default Merperson movement (to be overridden)."""
        super().swim(max_x, max_y)

        # Occasionally swim upward
        if random.random() < 0.1:
            self.y -= 1  # Move up
        elif random.random() < 0.2:
            self.y += 1  # Move down

        # Keep within bounds
        self.x = max(0, min(self.x, max_x - self.width))
        self.y = max(1, min(self.y, max_y - 2))

    def reproduce_with(self, other) -> Optional["AquaticCreature"]:
        """Creates a new baby with a chance for mutation."""
        if not self.can_reproduce(other):
            return None

        baby_x, baby_y = self.find_nearest_open_space((self.x + other.x) // 2, (self.y + other.y) // 2, self.bowl)

        offspring_type = random.choice([self.__class__, other.__class__])

        baby = offspring_type.create_offspring(f"{offspring_type.__name__}_Jr", self.bowl, baby_x, baby_y)

        if baby:
            self.last_reproduction_time = time.time()
            other.last_reproduction_time = time.time()
            self.eaten_since_last_reproduction = 0
            other.eaten_since_last_reproduction = 0
            self.offspring_count += 1
            other.offspring_count += 1

            self.bowl.log_activity(f"{self.emoji} {self.name} had a baby: {baby.name}!")

        return baby

    @property
    def stats(self):
        return {
            **super().stats,
            **{
                'Gender': self.gender,
            }
        }
