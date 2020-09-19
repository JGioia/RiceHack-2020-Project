import pygame
import os
import random
import math
import threading


def magnitude(vector):
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)


def normalize(vector):
    mag = magnitude(vector)
    if mag == 0:
        return vector
    return vector[0] / mag, vector[1] / mag


def scale(num, vector):
    return num * vector[0], num * vector[1]


def add(vector1, vector2):
    return vector1[0] + vector2[0], vector1[1] + vector2[1]


class Person:
    MAX_ACTION_TIME = 30
    MIN_ACTION_TIME = 10

    MISCHIEF_FACTOR = 0.1
    AVOIDANCE_FACTOR = -10
    RANDOM_FACTOR = 0.1

    MOVE_CHANCE = 0.01
    STOP_CHANCE = 0.01
    MIN_SPEED = 1
    MAX_SPEED = 2

    BEHAVING = 0
    MISCHIEF = 1
    HALF_MASK = 2
    NO_MASK = 3
    SNEEZING = 4
    FEVER = 5

    def __init__(self, pos: tuple, sprite: str, behavior_dict: dict, screen_size: tuple):
        self._timer = 0
        self._pos = pos
        self._sprite = sprite
        self._behavior_dict = behavior_dict
        self._behavior_type = Person.BEHAVING
        self._direction = (0, 0)
        self._speed = 0
        self._bounds = screen_size
        self._last_nbr = None

    def tick(self, nbr):
        self._timer -= 1
        if self._timer <= 0:
            if self._behavior_type == Person.BEHAVING:
                self._behavior_type = self._determine_behavior()
            self._timer = random.randrange(Person.MIN_ACTION_TIME, Person.MAX_ACTION_TIME)
        self._determine_direction(nbr)
        if self._speed == 0 and random.random() < Person.MOVE_CHANCE:
            self._start()
        elif self._speed != 0 and random.random() < Person.STOP_CHANCE:
            self._stop()
        self._move()

    def _move(self):
        self._pos = add(self._pos, self._direction)
        x = self._pos[0]
        y = self._pos[1]
        if x < 0:
            x = 0
        if x > self._bounds[0]:
            x = self._bounds[0]
        if y < 0:
            y = 0
        if y > self._bounds[0]:
            y = self._bounds[0]
        self._pos = (x, y)

    def _start(self):
        self._speed = random.random() * (Person.MAX_SPEED - Person.MIN_SPEED) + Person.MIN_SPEED

    def _stop(self):
        self._speed = 0

    def _determine_behavior(self):
        rand_val = random.random()
        prob_sum = 0
        for b, p in self._behavior_dict.items():
            prob_sum += p
            if rand_val < prob_sum:
                return b
        return Person.BEHAVING

    def _determine_direction(self, nbr):
        direct = self._direction
        angle = random.random() * 2 * math.pi
        rand_direct = (math.cos(angle), math.sin(angle))
        nbr_direct = add(nbr.get_pos(), scale(-1, self._pos))
        direct = add(direct, scale(Person.RANDOM_FACTOR, rand_direct))
        if magnitude(nbr_direct) != 0:
            if self._behavior_type == Person.MISCHIEF:
                direct = add(direct, scale(Person.MISCHIEF_FACTOR, normalize(nbr_direct)))
            else:
                direct = add(direct, scale(Person.AVOIDANCE_FACTOR / magnitude(nbr_direct) ** 2, nbr_direct))
        self._direction = normalize(direct)

    def get_pos(self):
        return tuple(int(x) for x in self._pos)

    def get_is_misbehaving(self):
        return self._behavior_type <= 1

    def fix_behavior(self):
        self._behavior_type = 0

    def get_sprite(self):
        return self._sprite

    def get_condition(self):
        return self._behavior_type

test_behavior = {Person.MISCHIEF: 1}
a = Person((0, 0), "a", {Person.BEHAVING: 0}, (750, 750))
b = Person((750, 750), "a", test_behavior, (750, 750))
def reset_timer():
    a.tick(b)
    b.tick(a)
    threading.Timer(0.01, lambda: reset_timer()).start()
reset_timer()
while True:
     print(a.get_pos(), b.get_pos())
