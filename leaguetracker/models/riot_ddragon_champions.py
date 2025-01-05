"""This module contains the Pydantic models for the Riot DDragon API"""
from typing import List
from pydantic import BaseModel

class Info(BaseModel):
    """Model for the Riot DDragon champion info"""
    attack: int
    defense: int
    magic: int
    difficulty: int

class Image(BaseModel):
    """Model for the Riot DDragon champion image"""
    full: str
    sprite: str
    group: str
    x: int
    y: int
    w: int
    h: int

class Stats(BaseModel):
    """Model for the Riot DDragon champion stats"""
    hp: float
    hpperlevel: float
    mp: float
    mpperlevel: float
    movespeed: float
    armor: float
    armorperlevel: float
    spellblock: float
    spellblockperlevel: float
    attackrange: float
    hpregen: float
    hpregenperlevel: float
    mpregen: float
    mpregenperlevel: float
    crit: float
    critperlevel: float
    attackdamage: float
    attackdamageperlevel: float
    attackspeedperlevel: float
    attackspeed: float

class Champion(BaseModel):
    """Model for the Riot DDragon champion"""
    version: str
    id: str
    key: str
    name: str
    title: str
    blurb: str
    info: Info
    image: Image
    tags: List[str]
    partype: str
    stats: Stats

class RiotDDragonChampions(BaseModel):
    """Model for the Riot DDragon champions"""
    type: str
    format: str
    version: str
    data: dict[str, Champion]