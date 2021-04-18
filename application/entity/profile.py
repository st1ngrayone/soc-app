from dataclasses import dataclass


@dataclass
class Profile:
    birth_date: int
    email: str
    gender: str
    name: str
    lastname: str
    city: str
