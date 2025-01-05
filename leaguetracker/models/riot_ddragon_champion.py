# generated by datamodel-codegen:
#   filename:  Aatrox.json
#   timestamp: 2025-01-05T06:42:29+00:00

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Image(BaseModel):
    """Model for the Riot DDragon champion image"""
    full: str
    sprite: str
    group: str
    x: int
    y: int
    w: int
    h: int


class Skin(BaseModel):
    """Model for the Riot DDragon champion skin"""
    id: str
    num: int
    name: str
    chromas: bool


class Info(BaseModel):
    """Model for the Riot DDragon champion info"""
    attack: int
    defense: int
    magic: int
    difficulty: int


class Stats(BaseModel):
    """Model for the Riot DDragon champion stats"""
    hp: int
    hpperlevel: int
    mp: int
    mpperlevel: int
    movespeed: int
    armor: int
    armorperlevel: float
    spellblock: int
    spellblockperlevel: float
    attackrange: int
    hpregen: int
    hpregenperlevel: float
    mpregen: int
    mpregenperlevel: int
    crit: int
    critperlevel: int
    attackdamage: int
    attackdamageperlevel: int
    attackspeedperlevel: float
    attackspeed: float


class Leveltip(BaseModel):
    """Model for the Riot DDragon champion spell leveltip"""
    label: List[str]
    effect: List[str]


class Spell(BaseModel):
    """Model for the Riot DDragon champion spell"""
    id: str
    name: str
    description: str
    tooltip: str
    leveltip: Leveltip
    maxrank: int
    cooldown: List[int]
    cooldownBurn: str
    cost: List[int]
    costBurn: str
    datavalues: Dict[str, Any]
    effect: List[Optional[List[int]]]
    effectBurn: List[Optional[str]]
    vars: List
    costType: str
    maxammo: str
    range: List[int]
    rangeBurn: str
    image: Image
    resource: str


class Passive(BaseModel):
    """Model for the Riot DDragon champion passive"""
    name: str
    description: str
    image: Image


class Champion(BaseModel):
    """Model for the Riot DDragon champion"""
    id: str
    key: str
    name: str
    title: str
    image: Image
    skins: List[Skin]
    lore: str
    blurb: str
    allytips: List[str]
    enemytips: List[str]
    tags: List[str]
    partype: str
    info: Info
    stats: Stats
    spells: List[Spell]
    passive: Passive
    recommended: List


class RiotDDragonChampion(BaseModel):
    """Model for the Riot DDragon champion"""
    type: str
    format: str
    version: str
    data: dict[str, Champion]
