import random
import time
from typing import Optional
from wcwidth import wcswidth


class AquaticCreature:
    """Base class for all creatures."""

    REPRODUCTION_THRESHOLD = 3  # Number of food before reproduction
    REPRODUCTION_COOLDOWN = 15  # Seconds before breeding again
    RARITY_CHANCE = 0.25
    FULL_AT_FOOD_COUNT = 5
    REMOVE_FOOD_EVERY = 20

    NORMAL_EMOJIS = []
    RARE_EMOJIS = []
    ALLOW_RARE = True

    AVAILABLE_SEXES = ["Male", "Female"]

    def __init__(self, name: str, bowl: 'Bowl', emoji: str, x: int | None = None, y: int | None = None,
                 rare: bool = False) -> None:
        self.name = name
        self.bowl = bowl
        self.x = x
        self.y = y
        self.emoji = emoji
        # self.width = 2  # Emojis take up two spaces in most terminals
        self.rare = rare

        # Age Tracking
        self.birth_time = time.time()

        # Fullness Tracking
        self.last_food_removed = self.birth_time
        self.current_food_count = 0

        # ✅ Reproduction Tracking
        self.eaten_since_last_reproduction = 0
        self.last_reproduction_time = 0
        self.offspring_count = 0

        self.sex = random.choice(self.AVAILABLE_SEXES)

    @property
    def is_full(self):
        return self.current_food_count >= self.FULL_AT_FOOD_COUNT

    @property
    def stats(self):
        if self.is_full:
            status = f"Full"
        else:
            status = f"{self.FULL_AT_FOOD_COUNT - self.current_food_count} food until full"
        return {
            'Name': self.name,
            'Age': self.age(),
            'Status': status,
            'Offspring': self.offspring_count,
            'Rarity': 'Rare!' if self.rare else '',
            'Sex': self.sex,
        }

    def can_reproduce(self, other: "AquaticCreature") -> bool:
        """Checks if two creatures can reproduce."""
        same_species = False
        for base1 in self.__class__.__bases__:
            for base2 in other.__class__.__bases__:
                if issubclass(base1, base2) or issubclass(base2, base1):
                    same_species = True
        return (
                same_species  # ✅ Must be the same species
                and time.time() - self.last_reproduction_time > self.REPRODUCTION_COOLDOWN
                and time.time() - other.last_reproduction_time > other.REPRODUCTION_COOLDOWN
                and self.eaten_since_last_reproduction >= self.REPRODUCTION_THRESHOLD
                and other.eaten_since_last_reproduction >= other.REPRODUCTION_THRESHOLD
        )

    def reproduce_with(self, other) -> Optional["AquaticCreature"]:
        """Creates a new baby with a chance for mutation."""
        if not self.can_reproduce(other):
            return None

        baby_x, baby_y = self.find_nearest_open_space((self.x + other.x) // 2, (self.y + other.y) // 2, self.bowl)

        baby_name = f"{self.name}_Jr"

        baby = self.create_offspring(baby_name, self.bowl, baby_x, baby_y)

        if baby:
            self.last_reproduction_time = time.time()
            other.last_reproduction_time = time.time()
            self.eaten_since_last_reproduction = 0
            other.eaten_since_last_reproduction = 0
            self.offspring_count += 1
            other.offspring_count += 1

            self.bowl.log_activity(f"{self.emoji} {self.name} had a baby: {baby.name}!")

        return baby

    def stay_in_bounds(self) -> None:
        """Ensures the creature stays within the tank boundaries."""
        emoji_width = len(self.emoji) * 2  # Account for emoji width
        self.x = max(1, min(self.x, self.bowl.width - emoji_width - 2))  # Keep inside width
        self.y = max(1, min(self.y, self.bowl.height - 2))  # ✅ Ensure creature doesn't exceed tank height

    def age(self) -> int:
        """Returns the creature's age in seconds."""
        return int(time.time() - self.birth_time)

    @property
    def closest_food(self):
        return min(
            self.bowl.cookies,
            key=lambda c: abs(self.x - c.x) + abs(self.y - c.y),
            default=None
        )

    def update(self) -> None:
        """Common update behavior for all creatures."""

        # ✅ Call swim() so creatures actually move
        self.swim(self.bowl.width - 2, self.bowl.height - 2)

        if time.time() > self.last_food_removed + self.REMOVE_FOOD_EVERY and self.current_food_count > 0:
            self.last_food_removed = time.time()
            self.current_food_count -= 1

        # ✅ If the creature reaches food, it eats it
        if self.closest_food and self.x == self.closest_food.x and self.y == self.closest_food.y:
            self.current_food_count += 1
            self.eaten_since_last_reproduction += 1
            self.bowl.log_activity(f"{self.emoji} {self.name} ate food!")
            self.closest_food.eat()

    def swim(self, max_x: int, max_y: int) -> None:
        """Creatures move toward the closest food, but avoid overlapping and stop when full."""

        if self.closest_food and not self.is_full:
            self.move_toward(self.closest_food.x, self.closest_food.y)  # ✅ Always move toward food if it exists
        else:
            # ✅ If no food, move randomly but avoid collisions
            potential_moves = [
                (self.x + dx, self.y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            ]
            occupied = self.bowl.get_occupied_positions()
            valid_moves = [move for move in potential_moves if
                           move not in occupied and 1 <= move[0] < max_x - 1 and 1 <= move[1] < max_y - 1]

            if valid_moves:
                self.x, self.y = random.choice(valid_moves)  # ✅ Only move randomly if no food exists

    def move_toward(self, target_x: int, target_y: int) -> None:
        """Move toward a specific target position while avoiding occupied spaces."""
        occupied = self.bowl.get_occupied_positions()

        # ✅ Compute best move toward the target
        potential_moves = sorted([
            (self.x + 1, self.y),  # Right
            (self.x - 1, self.y),  # Left
            (self.x, self.y + 1),  # Down
            (self.x, self.y - 1),  # Up
        ], key=lambda pos: abs(pos[0] - target_x) + abs(pos[1] - target_y))  # ✅ Prioritize best moves first

        # ✅ Filter out occupied or out-of-bounds moves
        valid_moves = [(x, y) for x, y in potential_moves if
                       (x, y) not in occupied and 1 <= x < self.bowl.width - 2 and 1 <= y < self.bowl.height - 2]

        # ✅ Choose the best available move
        if valid_moves:
            self.x, self.y = valid_moves[0]  # ✅ Pick the closest move to the target

    def random_movement(self) -> None:
        """Default random movement for creatures."""
        self.x += random.choice([-1, 0, 1])
        self.y += random.choice([-1, 0, 1])

    def find_nearest_open_space(self, x: int, y: int, bowl) -> tuple:
        """Finds the nearest available open space for a new creature."""
        occupied = bowl.get_occupied_positions()

        potential_positions = [
            (x + dx, y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]
            if (x + dx, y + dy) not in occupied and 1 <= x + dx < bowl.width - 2 and 1 <= y + dy < bowl.height - 2
        ]

        return random.choice(potential_positions) if potential_positions else (x, y)  # Stay in place if no free space

    @classmethod
    def create_offspring(cls, name: str, bowl: 'Bowl', x: int, y: int,
                         allow_rare: bool = False, rarity_chance: int | None = None):
        if type(cls) == AquaticCreature:
            raise NotImplementedError("Aquatic creatures can not directly create_offspring")
        return cls.create_creature(name=name, bowl=bowl, x=x, y=y, allow_rare=allow_rare, rarity_chance=rarity_chance)

    @classmethod
    def create_creature(cls, name: str, bowl: 'Bowl', x: int, y: int,
                        allow_rare: bool = False, rarity_chance: int | None = None) -> "AquaticCreature":
        """Creates a new creature with a chance of mutation."""
        if type(cls) == AquaticCreature:
            raise NotImplementedError('Aquatic creatures can not be directly created')

        if rarity_chance is None:
            rarity_chance = cls.RARITY_CHANCE
        inst = cls(name=name, bowl=bowl, x=x, y=y)
        if cls.ALLOW_RARE and allow_rare and random.random() < rarity_chance:
            inst.make_rare()
        return inst

    def make_rare(self):
        self.rare = True
        self.emoji = random.choice(self.RARE_EMOJIS)

    @classmethod
    def from_dict(cls, bowl: 'Bowl', data: dict):
        required_keys = ['name', 'x', 'y', 'rare', 'emoji']
        for x in required_keys:
            if x not in data:
                raise ValueError(f'Failed to recreate creature due to missing key: {x}')

        inst = cls.create_creature(name=data.get('name'), bowl=bowl, x=data.get('x'), y=data.get('y'))
        for key, value in data.items():
            if hasattr(inst, key):
                try:
                    setattr(inst, key, value)
                except AttributeError:
                    pass
        return inst

    def __dict__(self):
        return {
            'type': self.__class__.__name__,
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'emoji': self.emoji,
            'width': self.width,
            'rare': self.rare,

            # Age Tracking
            'birth_time': self.birth_time,

            # Fullness Tracking
            'last_food_removed': self.last_food_removed,
            'current_food_count': self.current_food_count,

            # ✅ Reproduction Tracking
            'eaten_since_last_reproduction': self.eaten_since_last_reproduction,
            'last_reproduction_time': self.last_reproduction_time,
            'offspring_count': self.offspring_count,
        }


    @property
    def width(self):
        """Determine the actual display width of the emoji."""
        return max(1, wcswidth(self.emoji))  # ✅ Correctly handles emoji widths
