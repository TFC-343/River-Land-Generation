import abc
import dataclasses
import random

import pygame


@dataclasses.dataclass
class Rule:
    """Flag class to store connection rules"""
    name: str


Blank = Rule("Blank")
WaterH = Rule("WaterH")
WaterV = Rule("WaterV")
PathH = Rule("PathH")
PathV = Rule("PathV")


@dataclasses.dataclass
class Rules:
    """stores all rules for a node"""
    north: Rule
    east: Rule
    south: Rule
    west: Rule

    def north_rule(self, other: 'Rules'):
        return self.north == other.south

    def east_rule(self, other: 'Rules'):
        return self.east == other.west

    def south_rule(self, other: 'Rules'):
        return self.south == other.north

    def west_rule(self, other: 'Rules'):
        return self.west == other.east


class Node:
    """store an image and associated rules"""
    def __init__(self, img, n, e, s, w):
        self.img = pygame.image.load(img)
        self.rules = Rules(n, e, s, w)


def get_nodes():
    """returns a list with all nodes"""
    nodes = [
        Node("WaveFunctionCollapse/images/0.png", Blank, Blank, Blank, Blank),  # blank tile
        Node("WaveFunctionCollapse/images/0a.png", Blank, Blank, Blank, Blank),  # blank tile
        Node("WaveFunctionCollapse/images/0b.png", Blank, Blank, Blank, Blank),  # blank tile
        Node("WaveFunctionCollapse/images/0c.png", Blank, Blank, Blank, Blank),  # blank tile

        Node("WaveFunctionCollapse/images/1.png", WaterV, Blank, WaterV, Blank),  # river up
        Node("WaveFunctionCollapse/images/2.png", Blank, WaterH, Blank, WaterH),  # river left

        Node("WaveFunctionCollapse/images/3.png", Blank, WaterH, WaterV, Blank),  # river curve up and right
        Node("WaveFunctionCollapse/images/4.png", WaterV, WaterH, Blank, Blank),  # river curve down and right
        Node("WaveFunctionCollapse/images/5.png", WaterV, Blank, Blank, WaterH),  # river curve left and up
        Node("WaveFunctionCollapse/images/6.png", Blank, Blank, WaterV, WaterH),  # river curve left and down

        Node("WaveFunctionCollapse/images/7.png", WaterV, PathH, WaterV, PathH),
        Node("WaveFunctionCollapse/images/9.png", PathV, WaterH, PathV, WaterH),
        Node("WaveFunctionCollapse/images/8.png", Blank, PathH, Blank, PathH),
        Node("WaveFunctionCollapse/images/10.png", PathV, Blank, PathV, Blank),

        Node("WaveFunctionCollapse/images/11.png", Blank, PathH, PathV, Blank),
        Node("WaveFunctionCollapse/images/12.png", PathV, PathH, Blank, Blank),
        Node("WaveFunctionCollapse/images/13.png", PathV, Blank, Blank, PathH),
        Node("WaveFunctionCollapse/images/14.png", Blank, Blank, PathV, PathH),
        # Node("WaveFunctionCollapse/images/15.png", PathV, PathH, PathV, PathH),
    ]

    return nodes


def rand_colour():
    """generates a random pygame colour"""
    return pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
