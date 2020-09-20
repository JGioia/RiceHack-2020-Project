import pygame
import os
import random
import time
from math import sqrt
#Need to figure out if I need to take this out.....
from person import Person

class Level:

    def __init__(self, numPeople, vioTime, spriteList, size, lives, levelTime, vioRange, behavior_dict, peoSize:tuple):
        self.numPeople = numPeople
        self.vioTime = vioTime
        self.size = size # Will size be given as a tuple, if so just change to include
        # index in the following functions
        self.lives = lives
        self.levelTime = levelTime
        self.startTime = time.time()
        self.people = []
        self.violators = {}
        self.vioRange = vioRange
        self.peoSize = peoSize

        for i in range(0, self.numPeople):
            # Once we know size of sprite we can adjust x_pos, so they can't be off screen
            # Top left corner of sprite is position
            x_pos = random.randint(0, self.size[0])
            y_pos = random.randint(self.size[1]//25, self.size[1]//(6/5))

            self.people[i] = Person((x_pos, y_pos), random.choice(spriteList), behavior_dict, size)

        # The initial setup for the violation times for each person object
        for person in range(0, self.numPeople):
            self.violators[person] = 0

    def tick(self):
        for person in range(0, self.numPeople):
            closestPer = self.closestToPerson(self.people[person])

            (self.people[person]).tick(closestPer[0])
            self.checkViolations()

    def getPeople(self):
        return self.people

    def restartViolation(self):
        for person in range(0, self.numPeople):
            self.violators[person] = 0

    def fixAllBehaviors(self):
        for person in range(0, self.numPeople):
            self.people[person].fix_behavior()

    def checkViolations(self):

        for person in range(0, self.numPeople):

            if (self.people[person].get_is_misbehaving()) or (self.checkDistanceViolation(self.people[person])):
                self.violators[person] += 1/60 # Need fix this, maybe request time in a tic.


            if (self.violators[person] >= self.vioTime):
                self.lives -= 1
                self.restartViolation()
                self.fixAllBehaviors()
                break


    def checkLost(self):
        if self.lives == 0:
            return True
        else:
            return False

    def checkWin(self):
        if (self.lives != 0) and (time.time() - self.startTime >= self.levelTime):
            return True
        else:
            return False

    def checkDistanceViolation(self, person):
            closest = self.closestToPerson(person)

            if closest[1] <= self.vioRange:
                return True
            else:
                return False

    def closestToPerson(self, person):

        personPosX = (self.people[person]).get_pos()[0]
        personPosY = (self.people[person]).get_pos()[1]

        closestPer = person - 1
        closestPerX = (self.people[closestPer]).get_pos()[0]
        closestPerY = (self.people[closestPer]).get_pos()[1]

        X_val = ((closestPerX + self.peoSize[0] // 2) - (personPosX + self.peoSize[0] // 2))**2
        Y_val = ((closestPerY + self.peoSize[0] // 2) - (personPosY + self.peoSize[1] // 2))**2
        closestDistance = sqrt(X_val + Y_val)

        for neighbor in range(0, self.numPeople):

            if neighbor == person:
                continue

            else:
                neighX = (self.people[neighbor]).get_pos()[0]
                neighY = (self.people[neighbor]).get_pos()[1]
                Distance = sqrt((neighX - personPosX) ** 2 + (neighY - personPosY) ** 2)

                if Distance < closestDistance:
                    closestPer = neighbor
                    closestDistance = sqrt((neighX - personPosX) ** 2 + (neighY - personPosY) ** 2)

        return self.people[closestPer], closestDistance

