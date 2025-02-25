import time
import json
import random
import os
import unicodedata
from wcwidth import wcswidth

from typing import List
from .cookie import Cookie
from .aquatic_creature import AquaticCreature
from .crab import Crab
from .fish import Fish
from .jellyfish import Jellyfish
from .shark import Shark
from .merman import Merman
from .mermaid import Mermaid
from .shrimp import Shrimp

AVAILABLE_CREATURES = {
    Fish: [4, 8],
    Crab: [4, 8],
    Jellyfish: [4, 8],
    Merman: [2, 3],
    Mermaid: [2, 3],
    Shrimp: [4, 8],
    Shark: [1, 1],
}


class Bowl:
    def __init__(self, width: int, height: int, save_file: str) -> None:
        self.width: int = width
        self.height: int = height
        self.save_file: str = save_file
        self.creatures: List[AquaticCreature] = []
        self.cookies: List[Cookie] = []  # 🍪 Multiple food items
        self.activity_log: List[str] = []  # Tracks last 3 actions
        self.paused: bool = False  # ✅ Track pause state

    def toggle_pause(self) -> None:
        """Toggle pausing of updates and rendering."""
        self.paused = not self.paused
        state = "Paused" if self.paused else "Resumed"
        self.log_activity(f"⏸ {state} the simulation.")

    def spawn_creature(self) -> None:
        """Spawns a new random non-shark creature."""
        creature_type = random.choice([Fish, Crab, Jellyfish])
        x = random.randint(1, self.width - 3)
        y = random.randint(1, self.height - 3)

        new_creature = creature_type.create_offspring(f"{creature_type.__name__}_{random.randint(100, 999)}", self, x,
                                                      y)
        self.creatures.append(new_creature)
        self.log_activity(f"✨ Spawned a new {new_creature.emoji} {new_creature.name}!")

    def kill_random_creature(self) -> None:
        """Removes a random non-shark creature, but ensures at least two of each species remain."""
        species_counts = {}  # ✅ Count how many of each species exist
        for creature in self.creatures:
            species_name = type(creature).__name__
            if species_name not in species_counts:
                species_counts[species_name] = 0
            species_counts[species_name] += 1

        # ✅ Create a list of creatures that can be removed
        removable_creatures = [
            c for c in self.creatures
            if not isinstance(c, Shark) and species_counts[type(c).__name__] > 2  # ✅ Ensure at least 2 remain
        ]

        if removable_creatures:
            victim = random.choice(removable_creatures)
            self.creatures.remove(victim)
            self.log_activity(f"💀 {victim.emoji} {victim.name} was removed from the tank.")
        else:
            self.log_activity("⚠️ Cannot remove any more creatures without causing extinction!")

    def log_activity(self, message: str) -> None:
        """Logs an activity and keeps only the last 3 events."""
        self.activity_log.append(message)
        if len(self.activity_log) > 3:
            self.activity_log.pop(0)  # Keep only the last 3 events

    def handle_reproduction(self) -> None:
        """Check for breeding pairs and spawn new creatures if conditions are met."""
        new_creatures = []

        for i, creature in enumerate(self.creatures):
            for j, other in enumerate(self.creatures):
                if i != j:  # ✅ Ensure different creatures
                    baby = creature.reproduce_with(other)
                    if baby:
                        new_creatures.append(baby)

        self.creatures.extend(new_creatures)

    def generate_waves(self) -> str:
        """Generate a random wave pattern for the top of the tank."""
        return ''.join(random.choice(['~', '=', ' ']) for _ in range(self.width - 2))

    def drop_food(self) -> None:
        """Drops a cookie in a random location near the center of the tank."""
        x_position = random.randint(self.width // 3, (self.width * 2) // 3)
        self.cookies.append(Cookie(x_position, self))  # 🍪 Add a new cookie!

    def update(self) -> None:
        """Updates all creatures, prevents overlapping, handles food, and enables reproduction."""
        # Make each cookie sink
        for cookie in self.cookies:
            cookie.update()

        # ✅ Call update on each creature
        for creature in self.creatures:
            creature.update()

        # ✅ Check for reproduction
        self.handle_reproduction()

    def render(self) -> str:
        """Render the fish tank with statistics and activity log while preventing overlapping creatures."""
        tank_lines: List[str] = []

        # Top of the tank with waves
        tank_lines.append("╔" + self.generate_waves() + "╗")

        # Middle section (empty space for creatures & food)
        for _ in range(self.height - 2):
            tank_lines.append("║" + " " * (self.width - 2) + "║")

        # Bottom of the tank
        tank_lines.append("╚" + "═" * (self.width - 2) + "╝")

        # ✅ Ensure creatures are placed without overwriting each other
        occupied_positions = set()

        for creature in sorted(self.creatures, key=lambda c: c.y):
            if 1 <= creature.y < len(tank_lines):  # ✅ Prevent out-of-range errors
                row = list(tank_lines[creature.y])
                emoji_chars = list(creature.emoji)
                emoji_width = creature.width  # ✅ Use correct forced width

                # ✅ Check if the space is occupied before placing the creature
                if all((creature.x + i, creature.y) not in occupied_positions for i in range(emoji_width)):
                    row[creature.x + 1: creature.x + 1 + emoji_width] = emoji_chars

                    # ✅ Mark occupied positions
                    occupied_positions.update((creature.x + i, creature.y) for i in range(emoji_width))

                tank_lines[creature.y] = ''.join(row)

        # ✅ Place cookies while ensuring they don't overlap creatures
        for cookie in self.cookies:
            if (cookie.x, cookie.y) not in occupied_positions:
                row = list(tank_lines[cookie.y])
                emoji_chars = list("🍪")  # ✅ Get correct width
                emoji_width = len(emoji_chars) * wcswidth('🍪')  # ✅ Handle emoji width

                # ✅ Ensure the cookie fits in the tank without shifting alignment
                if cookie.x + emoji_width < self.width - 2:
                    row[cookie.x + 1: cookie.x + 1 + emoji_width] = emoji_chars
                    occupied_positions.update((cookie.x + i, cookie.y) for i in range(emoji_width))

                tank_lines[cookie.y] = ''.join(row)

        # ✅ Stats Section
        stats_lines = [" Stats ".center(30, "-")]
        for creature in self.creatures:
            stats_lines.append(f"{creature.emoji} {creature.stats}")

        # ✅ Activity Log Section
        activity_lines = [" Activity Log ".center(30, "-")] + self.activity_log

        # ✅ Merge tank and stats properly
        combined_output = []
        max_tank_height = max(len(tank_lines), len(stats_lines))

        for i in range(max_tank_height):
            tank_part = tank_lines[i] if i < len(tank_lines) else " " * self.width
            stats_part = stats_lines[i] if i < len(stats_lines) else ""
            combined_output.append(f"{tank_part}   {stats_part}")

        return "\n".join(combined_output) + "\n" + "\n".join(activity_lines)

    def add_creature(self, creature: AquaticCreature) -> None:
        self.creatures.append(creature)

    def save_state(self) -> None:
        """Saves the tank's current state to a JSON file."""
        data = {
            "width": self.width,
            "height": self.height,
            "creatures": [
                creature.__dict__() for creature in self.creatures
            ],
            "cookies": [
                cookie.__dict__() for cookie in self.cookies
            ],
            "activity_log": self.activity_log
        }

        with open(self.save_file, "w") as file:
            json.dump(data, file, indent=4)

        print("💾 Tank state saved!")

    def load_state(self) -> None:
        """Loads the tank's state from a JSON file, or populates it with random creatures if no save exists."""
        if not os.path.exists(self.save_file):
            print("🚀 No save file found! Generating a new tank with random creatures.")
            self.populate_random_tank()
            return

        with open(self.save_file, "r") as file:
            data = json.load(file)

        available_types = {x.__name__: x for x in AVAILABLE_CREATURES}
        for creature_data in data.get("creatures", []):
            creature_type: AquaticCreature = available_types.get(creature_data.get('type', None), None)
            if creature_type:
                self.add_creature(creature_type.from_dict(self, creature_data))
        # Restore cookies
        self.cookies = [
            Cookie.from_dict(bowl=self, data=cookie) for cookie in data.get("cookies", [])
        ]
        # Restore activity log
        self.activity_log = data.get("activity_log", [])[-3:]  # Keep last 3 logs

        print("🔄 Tank state loaded!")

    def populate_random_tank(self) -> None:
        """Fills the tank with a random selection of creatures if no save exists."""
        for creature, spawn_rate in AVAILABLE_CREATURES.items():
            min_spawn, max_spawn = spawn_rate
            for _ in range(random.randint(min_spawn, max_spawn)):
                name = f"{creature.__name__}_{random.randint(100, 999)}"
                x = random.randint(1, self.width - 3)
                y = random.randint(1, self.height - 3)
                self.creatures.append(creature.create_creature(name, self, x, y, allow_rare=True))

        # Log the initial population
        self.log_activity("🌱 New tank populated with random creatures, including a predator!")

    def get_occupied_positions(self) -> set:
        """Returns a set of (x, y) positions currently occupied by creatures."""
        return {(creature.x, creature.y) for creature in self.creatures}
