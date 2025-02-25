import random
from typing import List, Optional
import time
from .aquatic_creature import AquaticCreature


class Shark(AquaticCreature):
    """A predator that hunts and eats other creatures but regulates population."""
    NORMAL_EMOJIS = ["🦈"]
    ALLOW_RARE = False
    HUNT_RADIUS = 5
    KILL_COOLDOWN = 3
    MIN_POPULATION = 10
    MAX_POPULATION = 12

    def __init__(self, name: str, bowl: 'Bowl', x: int | None = None, y: int | None = None) -> None:
        super().__init__(name=name, bowl=bowl, emoji=random.choice(self.NORMAL_EMOJIS), x=x, y=y)
        self.hunger = 0
        self.last_kill_time = 0

    def update(self) -> None:
        """Shark hunts prey but only if the population is high."""
        if len(self.bowl.creatures) <= self.MIN_POPULATION:
            return  # Stop hunting if population is too low

        prey = self.closest_food

        self.move_toward(prey.x, prey.y)

        # Kill prey if cooldown allows
        if self.x == prey.x and self.y == prey.y and (time.time() - self.last_kill_time) >= self.KILL_COOLDOWN:
            self.bowl.creatures.remove(prey)
            self.hunger += 1
            self.last_kill_time = time.time()
            self.bowl.log_activity(f"🦈 {self.name} ate {prey.name}!")

        self.stay_in_bounds()  # ✅ Keep sharks inside!

    @property
    def closest_food(self):
        return min(
            [c for c in self.bowl.creatures if not isinstance(c, Shark)],
            key=lambda c: abs(self.x - c.x) + abs(self.y - c.y),
            default=None
        )
