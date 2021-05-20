from Modules.player import Player
import pygame
import random

# defines the ghost class, which inherits from the player class


class Ghost(Player):

    # each ghost will spawn at the (x,y) passed to it
    def __init__(self, x, y, player):
        super(Ghost, self).__init__()
        # load image
        self.image = pygame.image.load("Resources\\GU1.png")

        self.player = player

        # the next 2 lines tell pygame where to begin drawing the ghosts
        self.rect.x, self.rect.y = x, y

        # list of directions each ghost may take
        self.directions = ["u", "d", "l", "r"]

        # assigns a random direction
        self.current_direction = self.directions[random.randint(0, 3)]

        self.previous_direction = ""

        self.weakened = False

        # dictionary which contains all pacman frames in every movement direction
        self.animation_dict = {"u": ["Resources\\GU1.png", "Resources\\GU2.png"],
                               "d": ["Resources\\GD1.png", "Resources\\GD2.png"],
                               "l": ["Resources\\GL1.png", "Resources\\GL2.png"],
                               "r": ["Resources\\GR1.png", "Resources\\GR2.png"],
                               "w": ["Resources\\WG1.png", "Resources\\WG2.png"]}

    def move(self, lvl):
        # checks if pacman entered any of the two portals
        self.check_portal()

        # 4 blocks of code
        # each one corresponds to a direction
        # up direction
        if self.current_direction == "u":
            self.rect.move_ip(0, -self.speed)
            self.previous_direction = "u"

        # down direction
        elif self.current_direction == "d":
            self.rect.move_ip(0, self.speed)
            self.previous_direction = "d"

        # left direction
        elif self.current_direction == "l":
            self.rect.move_ip(-self.speed, 0)
            self.previous_direction = "l"

        # right direction
        elif self.current_direction == "r":
            self.rect.move_ip(self.speed, 0)
            self.previous_direction = "r"

        self.update_animation(lvl)
        self.reposition(lvl)

    def reposition(self, lvl):

        # makes sure to set a constant distance between pacman and any other wall
        d = 2

        if self.current_direction == "u":
            self.rect.move_ip(0, -d)
            if not lvl.check_collision(self):
                self.rect.move_ip(0, d)

            else:

                while lvl.check_collision(self):
                    self.rect.move_ip(0, 1)

                self.rect.move_ip(0, d)
                self.change_direction()

        elif self.current_direction == "d":
            self.rect.move_ip(0, d)
            if not lvl.check_collision(self):
                self.rect.move_ip(0, -d)

            else:

                while lvl.check_collision(self):
                    self.rect.move_ip(0, -1)

                self.rect.move_ip(0, -d)
                self.change_direction()

        elif self.current_direction == "l":
            self.rect.move_ip(-d, 0)
            if not lvl.check_collision(self):
                self.rect.move_ip(d, 0)

            else:

                while lvl.check_collision(self):
                    self.rect.move_ip(1, 0)

                self.rect.move_ip(d, 0)
                self.change_direction()

        elif self.current_direction == "r":
            self.rect.move_ip(d, 0)
            if not lvl.check_collision(self):
                self.rect.move_ip(-d, 0)

            else:

                while lvl.check_collision(self):
                    self.rect.move_ip(-1, 0)

                self.rect.move_ip(-d, 0)
                self.change_direction()

    def update_animation(self, lvl):

        if not lvl.check_collision(self):

            if not self.weakened:
                # from the dictionary containing all images, select the current direction and decide which frame to use based on the animation index
                self.image = pygame.image.load(self.animation_dict[self.current_direction][self.animation_index])

            else:
                self.image = pygame.image.load(self.animation_dict["w"][self.animation_index])

        # if pacman is on his zero frame, move into the first frame
        if self.animation_index == 0:
            self.animation_index = 1

        # if pacman is on his first frame, move back into the zero frame
        else:
            self.animation_index = 0

    def check_player(self, offset):

        x = ""
        y = ""

        if 0 > (self.player.rect.x - self.rect.x) > -offset:
            x = "l"

        elif 0 < (self.player.rect.x - self.rect.x) < offset:
            x = "r"

        if 0 > (self.player.rect.y - self.rect.y) > -offset:
            y = "u"

        elif 0 < (self.player.rect.y - self.rect.y) < offset:
            y = "d"

        return [x, y]

    # function to change directions, chooses randomly between the 0-3 index
    def change_direction(self):

        temp = self.directions.copy()
        temp.remove(self.previous_direction)

        if self.weakened:

            try:
                if self.check_player(100)[0] == "l":
                    temp.remove("l")

                elif self.check_player(100)[0] == "r":
                    temp.remove("r")

                if self.check_player(100)[1] == "u":
                    temp.remove("u")

                elif self.check_player(100)[1] == "d":
                    temp.remove("d")

            except ValueError:
                pass

        self.current_direction = temp[random.randint(0, len(temp)-1)]
