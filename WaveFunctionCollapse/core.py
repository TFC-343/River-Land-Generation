import collections
import copy
import random
import sys

import pygame
from pygame.locals import *


from .helper import *


__all__ = ["game_loop"]

TILE_NUM = 10
TILE_SIZE = 100


class Tile:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.possible_nodes = get_nodes()

    def collapsed(self):
        return len(self.possible_nodes) == 1

    def draw(self, surf: pygame.Surface):
        if self.collapsed():
            surf.blit(pygame.transform.scale(self.possible_nodes[0].img, (TILE_SIZE, TILE_SIZE)),
                      (self.x * TILE_SIZE, self.y * TILE_SIZE))
        else:
            e = 3
            s = TILE_SIZE // e
            for i in range(0, min(e**2, len(self.possible_nodes))):
                surf.blit(pygame.transform.scale(self.possible_nodes[i].img, (s, s)),
                          (self.x * TILE_SIZE + s * (i % e), self.y * TILE_SIZE + s * (i // e)))


def in_range(x, y):
    return 0 <= x < TILE_NUM and 0 <= y < TILE_NUM


def collapse(tiles):
    unstable = [t for t in tiles if not t.collapsed()]
    if not unstable:
        return
    min_entropy = len(min(unstable, key=lambda x: len(x.possible_nodes)).possible_nodes)
    t = random.choice([u for u in unstable if len(u.possible_nodes) == min_entropy])
    t.possible_nodes = [random.choice(t.possible_nodes)]
    return t.x, t.y


def propagate(tiles, x, y, /, *,  visited=None):
    if visited is None:
        visited = []
    assert isinstance(visited, list)
    visited.append((x, y))
    counter = ((0, -1, "south_rule"),
               (1, 0, "west_rule"),
               (0, 1, "north_rule"),
               (-1, 0, "east_rule"))
    changed = False
    for i, j, rule in counter:
        if in_range(x + i, y + j):
            # visited.append((x + i, y + j))
            n_tile = get_tile(tiles, x + i, y + j)
            pos_copy = n_tile.possible_nodes[:]
            for node in pos_copy:
                allowed = False
                for c_node in get_tile(tiles, x, y).possible_nodes:
                    if node.rules.__getattribute__(rule)(c_node.rules):
                        allowed = True
                        break
                if not allowed:
                    n_tile.possible_nodes.remove(node)
                    changed = True
            if not n_tile.possible_nodes:
                print("uh oh")
                pygame.display.get_surface().fill("black")
                for t in tiles:
                    t.draw(pygame.display.get_surface())
                pygame.display.update()
                while pygame.event.wait().type != KEYDOWN:
                    ...
                for index, tile in enumerate(tiles):
                    tiles[index] = Tile(tile.x, tile.y)

    # if not changed:
    #     visited.append((x, y))

    for i, j, _ in counter:
        if in_range(x + i, y + j) and (x + i, y + j) not in visited:
            propagate(tiles, x + i, y + j, visited=visited)


def get_tile(tiles, x, y) -> Tile:
    return tiles[y * TILE_NUM + x]


def game_loop():
    tile_num = TILE_NUM
    tile_size = TILE_SIZE
    screen = pygame.display.set_mode((tile_size*tile_num, tile_size*tile_num))
    clock = pygame.time.Clock()

    tiles = [Tile(i % tile_num, i // tile_num) for i in range(tile_num**2)]

    stack_index = -1
    stack = []

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if (c := collapse(tiles)) is not None:
            propagate(tiles, c[0], c[1])

        screen.fill("black")
        for t in tiles:
            t.draw(screen)

        pygame.display.update()
        clock.tick(60)
