import os
import random
import math
# import threading


def normalize(vector):
    mag = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    if mag == 0:
        return vector
    return vector[0] / mag, vector[1] / mag


class Person:
    MAX_ACTION_TIME = 60
    MIN_ACTION_TIME = 20

    AVOIDANCE_FACTOR = 0.5

    MOVE_CHANCE = 0.4
    STOP_CHANCE = 0.4
    MAX_SPEED = 1

    BEHAVING = 0
    MISCHIEF = 1
    HALF_MASK = 2
    NO_MASK = 3
    SNEEZING = 4
    FEVER = 5

    def __init__(self, pos: tuple, sprite: str, behavior_dict: dict):
        self._timer = 0
        self._pos = pos
        self._sprite = sprite
        self._behavior_dict = behavior_dict
        self._behavior_type = Person.BEHAVING
        self._direction = (0, 0)
        self._speed = 0

    def tick(self, nbr):
        self._timer -= 1
        if self._timer <= 0:
            self._behavior_type = self._determine_behavior()
            self._determine_direction(nbr)
            self._timer = random.randrange(Person.MIN_ACTION_TIME, Person.MAX_ACTION_TIME)
        self._move()

    def _move(self):
        self._pos = (self._pos[0] + self._direction[0] * self._speed, self._pos[1] + self._direction[1] * self._speed)
        # TODO check if out of bounds and move back in bounds

    def _determine_behavior(self):
        rand_val = random.random()
        prob_sum = 0
        for b, p in self._behavior_dict.items():
            prob_sum += p
            if rand_val < prob_sum:
                return b
        return Person.BEHAVING

    def _determine_direction(self, nbr):
        direct = (0, 0)
        if self._speed == 0:
            if random.random() < Person.MOVE_CHANCE:
                self._speed = random.random() * Person.MAX_SPEED
            else:
                direct = self._direction
        if self._speed > 0:
            if random.random() < Person.STOP_CHANCE:
                self._speed = 0
            else:
                angle = random.random() * 2 * math.pi
                direct = (math.cos(angle), math.sin(angle))
        if self._speed > 0:
            nbr_direct = (nbr.get_pos()[0] - self._pos[0], nbr.get_pos()[1] - self._pos[1])
            nbr_direct = normalize(nbr_direct)
            if self._behavior_type == Person.MISCHIEF:
                direct = (direct[0] + Person.AVOIDANCE_FACTOR * nbr_direct[0],
                          direct[1] + Person.AVOIDANCE_FACTOR * nbr_direct[1])
            else:
                direct = (direct[0] - Person.AVOIDANCE_FACTOR * nbr_direct[0],
                          direct[1] - Person.AVOIDANCE_FACTOR * nbr_direct[1])
            self._direction = normalize(direct)

    def get_pos(self):
        return self._pos

    def get_is_misbehaving(self):
        return self._behavior_type <= 1

    def fix_behavior(self):
        self._behavior_type = 0

    def get_sprite(self):
        return self._sprite

    def get_condition(self):
        return self._behavior_type



# test_behavior = {Person.BEHAVING: .7, Person.MISCHIEF: .3}
# a = Person((0, 0), "a", test_behavior)
# b = Person((1, 0), "a", test_behavior)
# def reset_timer():
#     a.tick(b)
#     b.tick(a)
#     threading.Timer(0.01, lambda: reset_timer()).start()
# reset_timer()
# while True:
#     print(a.get_pos(), a._speed)
