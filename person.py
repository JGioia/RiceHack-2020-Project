import pygame
import os
import random


class Person:
    MAX_ACTION_TIME = 60
    MIN_ACTION_TIME = 20


    BEHAVING = 0
    MISCHIEF = 1
    HALF_MASK = 2
    NO_MASK = 3
    SNEEZING = 4
    FEVER = 5

    def __init__(self, pos, sprite, behavior_dict):
        self._timer = 0
        self._pos = pos
        self._sprite = sprite
        self._p_misbehave = p_misbehave
        self._behavior_type = Person.BEHAVING
        self._direction = (0, 0)
        self._speed = 0

    def tick(self, nbr):
        self._timer -= 1
        if self._timer == 0:
            self._determine_behavior()
        self._pos = (self._pos[0] + self._direction[0] * self._speed, self._pos[1] + self._direction[1] * self._speed)

    def _determine_behavior(self):
        if random.random() < self._p_misbehave:
            # TODO: Determine bad action
            # TODO: Change sprite to desired bad action
        else:
            # TODO: Determine direction of walking (AI)
            self._timer = random.randRange(Person.MIN_ACTION_TIME, Person.MAX_ACTION_TIME)

    def get_pos(self):
        return self._pos

    def get_is_misbehaving(self):
        return self._behavior_type <= 1

    def fix_behavior(self):
        self._behavior_type = 0
