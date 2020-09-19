import pygame
import os
from menu import Menu
from level import Level

# create window
pygame.font.init()
WIDTH, HEIGHT = 750, 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fun game")  # change this later

# load images
PERSON_1 = pygame.image.load(os.path.join("graphics", "placeholder_person"))
PERSON_2 = pygame.image.load(os.path.join("graphics", "placeholder_person2"))


def main():
    # initialize variables
    run = True
    FPS = 60
    level_num = 1
    level_dict = {1: (10, 0.1), 2: (15, 0.15)}  # maps level numbers to level object initiations
    level = Level(level_dict[level_num][0], level_dict[level_num][1])
    menu = Menu()
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans", 50)
    scene = "Level"
    sprites = []

    def decode_sprite(sprite_name, sprite_type=0, pos=(0, 0)):
        if sprite_name == "Level_Background":
            return PERSON_1, pos

    def redraw_window():
        nonlocal sprites
        sprites = []
        if scene == "Level":
            # get background
            sprites.append(decode_sprite(level.get_background_name()))

            # get people
            for person in level.get_people():
                sprites.append(decode_sprite(person.get_sprite_name(), person.get_sprite_type(), person.get_position()))

            # get text
            sprites.append((main_font.render(level.get_text(), 1, (0, 255, 255)), level.get_text_pos()))

        if scene == "Menu":
            # get background
            sprites.append(decode_sprite(menu.get_background()))

            # get rest of sprites

        for sprite in sprites:
            WINDOW.blit(sprite[0], sprite[1])

        pygame.display.update()

    def clicked_on():
        if pygame.mouse.get_pressed()[0]:
            for i in range(len(sprites) - 1, -1, -1):
                sprite = sprites[i]
                # check range
        return 0

    while run:
        # tick
        clock.tick(FPS)

        # check what has been clicked on
        clicked = clicked_on()

        # check if lost/won level
        if scene == "Level":
            if level.has_lost():
                scene = "menu"
            if level.has_won():
                scene = "menu"
                menu.unlock_next_level()

        # check if selected level
        if scene == "Menu" and menu.selected_level() != 0:
            level_num = menu.selected_level()
            level = Level(level_dict[level_num][0], level_dict[level_num][1])
            scene = "level"

        # tell level and menu what scene
        level.set_scene(scene)
        menu.set_scene(scene)

        # tick level and menu objects
        level.tick()
        menu.tick()

        # redraw window
        redraw_window()

        # quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


main()
