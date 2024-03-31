from pydantic import BaseModel, HttpUrl, validator
from typing import List, Optional
from enum import Enum


class Status(str, Enum):
    ALIVE = "Alive"
    DEAD = "Dead"
    UNKNOWN = "unknown"


class Gender(str, Enum):
    FEMALE = "Female"
    MALE = "Male"
    GENDERLESS = "Genderless"
    UNKNOWN = "unknown"


class CharacterFilter(BaseModel):
    name: Optional[str] = None
    status: Optional[Status] = None
    species: Optional[str] = None
    type: Optional[str] = None
    gender: Optional[Gender] = None
    page: Optional[int] = None


class Character(BaseModel):
    id: int
    name: str
    status: Status
    species: str
    type: str
    gender: Gender
    origin: dict
    location: dict
    image: HttpUrl
    episode: List[HttpUrl]
    url: HttpUrl
    created: str


class Episode(BaseModel):
    id: int
    name: str
    air_date: str
    episode: str
    characters: List[str]
    url: str
    created: str


class Location(BaseModel):
    id: int
    name: str
    type: str
    dimension: str
    residents: List[str]
    url: str
    created: str


class SurvivalRate(BaseModel):
    survival_rate: float
    total_characters: int


class SurvivalPrediction(BaseModel):
    location: str
    gender: str
    species: str
    predicted_survival_chance: float


class AtypicalEpisode(BaseModel):
    id: int
    name: str
    novel_pairings: int


class GroupedCharacters(BaseModel):
    origin: str
    characters: List[Character]


class CharacterAppearance(BaseModel):
    name: str
    appearances: int


class TopEpisode(BaseModel):
    count: int
    episode: Episode


class User:
    def __init__(self, username: str):
        self.username = username


mock_users_db = {
    "tomer": {
        "username": "tomer",
        "password": "password"
    }
}
