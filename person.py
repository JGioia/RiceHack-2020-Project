import pygame
import os
import random


class Person:
    MAX_ACTION_TIME = 60
    MIN_ACTION_TIME = 20

    def __init__(self, pos, sprite, p_misbehave):
        self._timer = 0
        self._pos = pos
        self._sprite = sprite
        self._p_misbehave = p_misbehave
        self._misbehaving = False
        self._direction = (0, 0)

    def tick(self, nbr):
        self._timer -= 1
        if self._timer == 0:
            self._determine_behavior()

    def _determine_behavior(self):
        if random.random() < self._p_misbehave:
            self._misbehaving = True
        else:
            self._timer = random.randRange(Person.MIN_ACTION_TIME, Person.MAX_ACTION_TIME)

    def get_pos(self):
        return self._pos

    def get_is_misbehaving(self):
        return self._misbehaving

    def fix_behavior(self):
        self._misbehaving = False