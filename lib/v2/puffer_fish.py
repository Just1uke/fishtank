from lib.v2.udlr_aquatic_creature import UDLRAquaticCreature
from lib.v2.aquatic_creature import Sexes
from enum import Enum
import random


class InflationState(Enum):
    INFLATED = "Inflated"
    DEFLATED = "Deflated"


class PufferFish(UDLRAquaticCreature):
    def __init__(self, tank: "FishTank", name: str, x: int = None, y: int = None):
        super().__init__(
            tank,
            name,
            x,
            y,
            sprite_sheet_path="assets/sprites.png",
            # animation_data=animation_data,
        )

        self._puffer_fish_state = None

        self.inflation_state = random.choice([InflationState.INFLATED, InflationState.DEFLATED])

    def update(self):
        super().update()
        if random.random() < .01:
            self.toggle_inflation_state()

    def toggle_inflation_state(self):
        if self.inflation_state == InflationState.INFLATED:
            self.inflation_state = InflationState.DEFLATED
        else:
            self.inflation_state = InflationState.INFLATED

    @property
    def inflation_state(self):
        return self._puffer_fish_state

    @inflation_state.setter
    def inflation_state(self, value: InflationState):
        self._puffer_fish_state = value
        animation_col = 0
        if value == InflationState.INFLATED:
            animation_col = 3

        if self.sex == Sexes.FEMALE:
            animation_col += 6

        self.animation_data = {
            "down": (0, animation_col, 3),
            "left": (1, animation_col, 3),
            "right": (2, animation_col, 3),
            "up": (3, animation_col, 3)
        }
        self.reload_animations()
