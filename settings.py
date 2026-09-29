import json
from dataclasses import dataclass, asdict


SETTINGS_FILE = "settings.json"


@dataclass
class PetSettings:
    size: int = 120
    speed: float = 2.0

    behavior: str = "auto"

    walk_on_windows: bool = True
    gravity_enabled: bool = True

    gravity: float = 0.5
    max_fall_speed: float = 15.0

    fly_speed: float = 3.0

    def save(self):
        with open(
            SETTINGS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                asdict(self),
                file,
                indent=4
            )

    @classmethod
    def load(cls):

        try:

            with open(
                SETTINGS_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            return cls(**data)

        except (
            FileNotFoundError,
            json.JSONDecodeError,
            TypeError
        ):

            return cls()