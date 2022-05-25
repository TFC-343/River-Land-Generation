import collections
import copy
import random
import sys

import pygame
from pygame.locals import *


from .helper import *


__all__ = ["game_loop"]

TILE_NUM = 10
TILE_SIZE = 50


class Tile:
    """stores all superpositions of a given grid space"""
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.possible_nodes = get_nodes()

    def collapsed(self):
        return len(self.possible_nodes) == 1

    def draw(self, surf: pygame.Surface):
        """draws the collapsed tile"""
        if self.collapsed():
            surf.blit(pygame.transform.scale(self.possible_nodes[0].img, (TILE_SIZE, TILE_SIZE)),
                      (self.x * TILE_SIZE, self.y * TILE_SIZE))


def in_range(x, y):
    """checks in a point would be on the grid"""
    return 0 <= x < TILE_NUM and 0 <= y < TILE_NUM


def collapse(tiles):
    """picks a random space from the grid with the lowest amount of superpositions and forces it to collapse"""
    unstable = [t for t in tiles if not t.collapsed()]  # gets a list of all un collapsed tiles
    if not unstable:
        return
    # finds the tile with the
    # lowest number of superpositions from the unstable list
    min_entropy = len(min(unstable, key=lambda x: len(x.possible_nodes)).possible_nodes)

    # randomly selects an options and selects it
    t = random.choice([u for u in unstable if len(u.possible_nodes) == min_entropy])
    t.possible_nodes = [random.choice(t.possible_nodes)]
    return t.x, t.y  # returns the position that was collapsed


def propagate(tiles, x, y, /, *,  visited=None):
    """recursively loops through all tiles and makes sure only legal superpositions remain"""
    # the list of visited positions stored each position in the grid that we have already checked around
    if visited is None:
        visited = []
    assert isinstance(visited, list)
    visited.append((x, y))
    counter = ((0, -1, "south_rule"),
               (1, 0, "west_rule"),
               (0, 1, "north_rule"),
               (-1, 0, "east_rule"))
    for i, j, rule in counter:  # propagates to the north, east, south, west
        if in_range(x + i, y + j):  # if the coords are in the grid
            n_tile = get_tile(tiles, x + i, y + j)  # gets the tile we are checking
            pos_copy = n_tile.possible_nodes[:]  # creates a copy of the superpositions to loop over
            for node in pos_copy:
                allowed = False  # a flag checking if the superposition is allowed to stay
                # loops through all superpositions of the current node and checks if they are compatible
                for c_node in get_tile(tiles, x, y).possible_nodes:
                    if node.rules.__getattribute__(rule)(c_node.rules):  # if at least one is, change flag
                        allowed = True
                        break
                if not allowed:  # if flag was not set, remove from super positions
                    n_tile.possible_nodes.remove(node)

            # sometimes the code will find that there are no possible states for a tile
            # this probably shouldn't happen and shows that there is an error in the propagation method
            # here I have added an error catcher while I fix it
            if not n_tile.possible_nodes:  # if all superpositions have been removed (ei. no legal state for the tile)
                print("Warning: Illegal state, restarting...", file=sys.stderr)
                for index, tile in enumerate(tiles):  # reset grid
                    tiles[index] = Tile(tile.x, tile.y)

    for i, j, _ in counter:  # then run the same algorithm on all adjacent grid spaced (as long as they have not already been visited)
        if in_range(x + i, y + j) and (x + i, y + j) not in visited:
            propagate(tiles, x + i, y + j, visited=visited)


def get_tile(tiles, x, y) -> Tile:
    """allows use of tiles list like a 2d list"""
    return tiles[y * TILE_NUM + x]


def game_loop():
    tile_num = TILE_NUM
    tile_size = TILE_SIZE
    screen = pygame.display.set_mode((tile_size*tile_num, tile_size*tile_num))
    clock = pygame.time.Clock()

    tiles = [Tile(i % tile_num, i // tile_num) for i in range(tile_num**2)]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if (c := collapse(tiles)) is not None:
            propagate(tiles, c[0], c[1])

        for t in tiles:
            t.draw(screen)

        pygame.display.update()
        clock.tick(60)
