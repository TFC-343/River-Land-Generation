import typing

import pygame


class Rule:
    def __init__(self, name: str): ...

Blank: Rule
WaterH: Rule
WaterV: Rule
PathH: Rule
PathV: Rule


class Rules:
    def __init__(self,
                 north: Rule,
                 east: Rule,
                 south: Rule,
                 west: Rule): ...

    north: Rule
    east: Rule
    south: Rule
    west: Rule

    def north_rule(self, other: Rules): ...
    def east_rule(self, other: Rules): ...
    def south_rule(self, other: Rules): ...
    def west_rule(self, other: Rules): ...


class Node:
    def __init__(self,
                 img: str,
                 north: Rule,
                 east: Rule,
                 south: Rule,
                 west: Rule
                 ): ...
    img: pygame.Surface
    rules: Rules

def get_nodes() -> typing.List[Node, ...]: ...

def rand_colour() -> pygame.Color: ...
