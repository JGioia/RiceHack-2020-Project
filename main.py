import pygame
import os
# from menu import Menu
from level import Level
from person import Person

# create window
pygame.font.init()
SCREEN_SIZE = (750, 750)
WINDOW = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Fun game")  # change this later

# load images
PEOPLE_NAMES = ["brian", "daniel", "joseph", "kami", "lauren", "liam", "peter", "steven", "yannie"]
PEOPLE_IMGS = []
PERSON_SIZE = (60, 100)
for person_name in PEOPLE_NAMES:
    PERSON_IMGS = []
    PERSON_IMGS.append(pygame.transform.scale(pygame.image.load(os.path.join("graphics", "Masked Sprites", person_name +
                                                                             "masked.png")), PERSON_SIZE))
    PERSON_IMGS.append([])
    PERSON_IMGS.append(pygame.transform.scale(pygame.image.load(os.path.join("graphics", "Wrongly Masked Sprites",
                                                                              person_name + "maskedincorrectly.png")),
                                               PERSON_SIZE))
    PERSON_IMGS.append(pygame.transform.scale(pygame.image.load(os.path.join("graphics", "Unmasked Sprites", person_name
                                                                             + "unmasked.png")), PERSON_SIZE))
    PERSON_IMGS.append(pygame.transform.scale(pygame.image.load(os.path.join("graphics", "Coughing Sprites", person_name
                                                                             + "coughing.png")), PERSON_SIZE))
    PERSON_IMGS.append(pygame.transform.scale(pygame.image.load(os.path.join("graphics", "Feverish Sprites", person_name
                                                                             + "feverish.png")), PERSON_SIZE))
    PEOPLE_IMGS.append(PERSON_IMGS)

PERSON_1 = pygame.transform.scale(pygame.image.load(os.path.join("graphics", "placeholder_person.jpg")), SCREEN_SIZE)
PERSON_2 = pygame.image.load(os.path.join("graphics", "placeholder_person2.jpg"))


def main():
    # initialize variables
    run = True
    FPS = 60
    sprite_list = ["a", "b"]
    starting_lives = 3
    level_time = 30
    vio_range = 100
    behavior_dict = {Person.MISCHIEF: 0.1, Person.NO_MASK: 0.1}
    level_num = 1
    num_people_dict = {1: 10, 2: 15}
    vio_time = 5
    level_size = (SCREEN_SIZE[0] - PERSON_SIZE[0] + 10, SCREEN_SIZE[1] - PERSON_SIZE[1] + 10)
    level = Level(num_people_dict[level_num], vio_range, PEOPLE_NAMES, level_size, starting_lives,
                  level_time, vio_time, behavior_dict, PERSON_SIZE)
    # menu = Menu()
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans", 50)
    scene = "Level"
    sprites = []
    sprite_objs = []

    def decode_sprite(sprite_name, pos=(0, 0), sprite_type=0):
        if sprite_name == "Level_Background":
            return PERSON_1, pos
        elif sprite_name == "Menu_Background":
            return PERSON_1, pos
        elif sprite_name == "a":
            return PERSON_1, pos
        elif sprite_name == "b":
            return PERSON_2, pos
        else:
            return PEOPLE_IMGS[PEOPLE_NAMES.index(sprite_name)][sprite_type], pos

    def redraw_window():
        nonlocal sprites
        sprites = []
        nonlocal sprite_objs
        sprite_objs = []
        if scene == "Level":
            # get background
            WINDOW.blit(decode_sprite("Level_Background")[0], decode_sprite("Level_Background")[1])

            # get people
            for person in level.getPeople():
                sprites.append(decode_sprite(person.get_sprite(), person.get_pos(), person.get_condition()))
                sprite_objs.append(person)
                person_center = (person.get_pos()[0] + PERSON_SIZE[0]//2, person.get_pos()[1] + PERSON_SIZE[1]//2)
                pygame.draw.circle(WINDOW, (0, 200, 131), person_center, 100, 10)

            # get text
            sprites.append((main_font.render(level.getText()[0], 1, (0, 255, 255)), level.getText()[1]))
            sprite_objs.append(0)

        if scene == "Menu":
            # get background
            sprites.append(decode_sprite("Menu_Background"))
            sprite_objs.append(0)

            # get rest of sprites

        for sprite in sprites:
            WINDOW.blit(sprite[0], sprite[1])

        pygame.display.update()

    def clicked_on():
        if pygame.mouse.get_pressed()[0]:
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]
            for i in range(len(sprites) - 1, -1, -1):
                sprite = sprites[i]
                if ((sprite_objs[i] != 0 and mouse_x >= sprite[1][0] and mouse_y >= sprite[1][1]) and
                        (mouse_x <= sprite[1][0] + sprite[0].get_width() and mouse_y <= sprite[1][1] +
                         sprite[0].get_height())):
                    sprite_objs[i].clicked_on()
                    pass
        pass

    while run:
        # tick
        clock.tick(FPS)

        # check what has been clicked on
        clicked_on()

        # check if lost/won level
        if scene == "Level":
            if level.checkLost():
                scene = "menu"
            if level.checkWin():
                scene = "menu"
                # menu.unlock_next_level()

        # check if selected level
        # if scene == "Menu" and menu.selected_level() != 0:
        #     level_num = menu.selected_level()
        #     level = Level(level_dict[level_num][0], level_dict[level_num][1])
        #     scene = "level"

        # tick level and menu objects
        if scene == "Level":
            level.tick()
        # elif scene == "Menu":
        #     menu.tick()

        # redraw window
        redraw_window()

        # quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


main()
