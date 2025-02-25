from lib.v2.udlr_aquatic_creature import UDLRAquaticCreature


class Stingray(UDLRAquaticCreature):
    def __init__(self, tank: "FishTank", name: str, x: int = None, y: int = None):
        super().__init__(
            tank,
            name,
            x,
            y,
            sprite_sheet_path="assets/sprites.png",
            animation_data={
                "down": (4, 6, 3),
                "right": (5, 6, 3),
                "left": (6, 6, 3),
                "up": (7, 6, 3)
            },
        )

    def update(self):
        super().update()
        min_height = self.tank.height // 6 * 5  # Bottom sixth starts here
        max_height = self.tank.height  # Absolute bottom of the tank

        if self.y >= max_height:
            self.y = max_height
            self.dy = -abs(self.dy)  # Move upward

        elif self.y <= min_height:
            self.y = min_height
            self.dy = abs(self.dy)  # Move downward
