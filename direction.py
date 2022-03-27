import pygame
from enum import Enum, auto

class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    FORWARD = auto()
    BACKWARD = auto()

    @classmethod
    def opposite(cls, direction):
        match direction:
            case cls.LEFT: return cls.RIGHT
            case cls.RIGHT: return cls.LEFT
            case cls.UP: return cls.DOWN
            case cls.DOWN: return cls.UP
            case cls.FORWARD: return cls.BACKWARD
            case cls.BACKWARD: return cls.FORWARD
            case _: return None

    @classmethod
    def from_key(cls, key):
        match key:
            case pygame.K_LEFT: return cls.LEFT
            case pygame.K_RIGHT: return cls.RIGHT
            case pygame.K_UP: return cls.UP
            case pygame.K_DOWN: return cls.DOWN
            case _: return None
