import pygame
import os


class Menu:

    def __init__(self, doors, stairs):
        self._floor = 0
        self._cleared = {door: False for door in doors}
        self._selected_door = None
        self._stairs = stairs
        self._nums = {door: num + 1 for num, door in enumerate(doors)}
        print(self._nums)

    def unlock_next_level(self):
        if self._selected_door != None:
            self._cleared[self._selected_door] = True
            self._selected_door = 0

    def selected_level(self):
        return self._floor * 4 + self._nums[self._selected_door] if (self._selected_door is not None) else 0

    def clicked_on(self, button):
        if button == self._stairs:
            if not self.get_floor_completed():
                return
            self._floor += 1
            for door in self._cleared:
                self._cleared[door] = False
        elif not self._cleared[button]:
            self._selected_door = button

    def get_floor(self):
        return self._floor

    def get_is_completed(self, door):
        return self._cleared[door]

    def get_floor_completed(self):
        for door in self._cleared:
            if not self._cleared[door]:
                return False
        return True


# menu = Menu(["1", "2", "3", "4"], "Stairs")
# menu.clicked_on("1")
# menu.unlock_next_level()
# menu.clicked_on("2")
# print(menu.selected_level())