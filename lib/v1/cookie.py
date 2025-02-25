import time


class Cookie:
    """Represents food dropped into the tank that sinks slowly and attracts fish."""
    MAX_LIFE = 5

    def __init__(self, x: int, bowl: 'Bowl') -> None:
        self.created = time.time()
        self.x: int = x
        self.y: int = 1  # Start just below the waves
        self.eaten_count: int = 0  # Number of times fish have touched it
        self.bowl = bowl

    def update(self) -> None:
        self.fall()
        if time.time() - self.created >= self.MAX_LIFE:
            self.bowl.cookies.remove(self)

    def fall(self) -> None:
        """Cookie sinks down one row per frame."""
        if self.y < self.bowl.height - 2:
            self.y += 1  # Moves down slowly

    def eat(self) -> bool:
        """Returns True if the cookie has been eaten enough times."""
        if self.eaten_count >= 5:
            self.bowl.cookies.remove(self)

    def __dict__(self):
        return {
            'created': self.created,
            'x': self.x,
            'y': self.y,
            'eaten_count': self.eaten_count,
        }

    @classmethod
    def from_dict(cls, bowl: 'Bowl', data: dict):
        required_keys = ['x', 'y', 'eaten_count', 'created']
        for x in required_keys:
            if x not in data:
                raise ValueError(f'Failed to recreate cookie due to missing key: {x}')
        inst = cls(data.get('x'), bowl=bowl)

        for key, value in data.items():
            if hasattr(inst, key):
                setattr(inst, key, value)
        return inst

