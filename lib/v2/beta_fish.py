from lib.v2.udlr_aquatic_creature import UDLRAquaticCreature
from lib.v2.aquatic_creature import Sexes


class BetaFish(UDLRAquaticCreature):
    def __init__(self, tank: "FishTank", name: str, x: int = None, y: int = None):
        super().__init__(
            tank,
            name,
            x,
            y,
            sprite_sheet_path="assets/sprites.png",
            # animation_data=animation_data,
        )
        start_col = 0
        if self.sex == Sexes.FEMALE:
            start_col = 3
        self.animation_data = {
            "down": (4, start_col, 3),  # Row 5, starts at column 0, 3 frames
            "left": (5, start_col, 3),  # Row 6, starts at column 0, 3 frames
            "right": (6, start_col, 3),  # Row 7, starts at column 0, 3 frames
            "up": (7, start_col, 3)  # Row 8, starts at column 0, 3 frames
        }


        self.reload_animations()

    def update(self):
        """Restrict movement to the top two-thirds of the tank."""
        super().update()
        max_height = self.tank.height * (2 / 3)

        if self.y >= max_height:
            self.y = max_height
            self.dy = -abs(self.dy)  # Move upward if at the boundary