# src/models.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict

# Defines the structure of the Player object
class Player(BaseModel):
    id: Optional[int] = Field(None)
    name: str
    time: int = Field(100)
    xp: int = Field(0)
    fun: int = Field(0)
    health: int = Field(50)
    stress: int = Field(0)

# Defines the structure of a Choice object
class Choice(BaseModel):
    id: Optional[int] = Field(None)
    name: str
    time_cost: int
    xp: int = Field(0)
    fun: int = Field(0)
    health: int = Field(0)
    stress: int = Field(0)

# Defines the structure of the API response after a game action
class GameActionResponse(BaseModel):
    player: Player
    game_over: bool = False
    ending_title: Optional[str] = None
    # We return the achievement data as a list of dictionaries to avoid creating a new Pydantic model
    achievement_unlocked: Optional[List[Dict]] = None