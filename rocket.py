from time import perf_counter as clock
from random import randint
from direction import Direction
from resources import Resources
from const import Const
from interstellar import Interstellar
from utils import Utils
import pygame


class Rocket(Interstellar):
    def __init__(self, spaceship, side):
        super().__init__(Resources.rocket, speed=0, x=0, y=0)
        self.spaceship = spaceship
        self.speed = (0, Const.ROCKET_INITIAL_SPEED)
        self.width, self.height = self.images[0].get_rect().size
        self.hitsize = (0, 0, self.width, self.height - Const.ROCKET_FLAME_SIZE)
        self.away = False
        self.next_frame = 0
        self.current_pic_num = 0
        self.on_board = True
        self.side = side
        self.launch_sound = Resources.wav_launch[0] if Resources.wav_launch else None
        self.x = 0
        self.y = 0

    def move(self):
        """
        If the rocket is on board, it will be moving with the spaceship
        on the x axis, and when fired - it will move on the y axis as well
        """
        if not self.is_launched():
            # The rocket is on board
            self.x, self.y = self.spaceship.get_xy()
            if self.side == Direction.left:
                self.x += Const.ROCKET_STOWED_OFFSET_X_LEFT
            else:
                self.x += Const.ROCKET_STOWED_OFFSET_X_RIGHT
            self.y += Const.ROCKET_STOWED_OFFSET_Y
            self.speed = (self.spaceship.get_horizontal_speed() / Const.ROCKET_HORIZONTAL_SPEED_DELTA, 0)
        else:
            # The rocket is on its way to the target
            if self.y > Const.OFF_THE_SCREEN_TOP:
                self.speed = tuple(map(sum, zip((0, Const.ROCKET_ACCELERATION), self.speed)))
                self.y -= self.speed[1]
                self.x += self.speed[0]
            else:
                self.away = True
        super().move()
        # If the rocket is gone from the screen (fly away or hit something), reload it
        if self.is_away():
            self.reload()

    def is_launched(self):
        """
        Return true if the rocket is launched
        """
        return not self.on_board

    def gone(self):
        """
        When the rocket hits something, it disappears
        """
        self.away = True

    def get_current_pic(self):
        """
        Return the current rocket image
        """
        if self.on_board:
            # The picture is static, without flame
            self.current_pic_num = 0
        else:
            # Change the picture
            if clock() > self.next_frame:
                # Make sure we're not randomly getting the same picture
                previous_number = self.current_pic_num
                while previous_number == self.current_pic_num:
                    self.current_pic_num = randint(1, len(self.images) - 1)
                self.next_frame = clock() + Const.FRAME_TIME_SEC
        return self.images[self.current_pic_num]

    def launch(self):
        """
        Launch the rocket - means detach it from the spaceship
        """
        if self.on_board:
            # Set the rocket angle depending on direction
            angle = -self.speed[0]*3
            if abs(angle) > 1:
                self.images = []
                for image in self.original_images:
                    self.images.append(Utils.rotate(image, angle))
            self.on_board = False
            if self.launch_sound:
                self.launch_sound.play()

    def reload(self):
        """
        Reset the rocket status, and attach it back to the spaceship
        """
        self.on_board = True
        self.away = False
        self.images = self.original_images
        self.speed = (0, Const.ROCKET_INITIAL_SPEED)

    def draw(self):
        """
        Draw the rocket
        """
        self.spaceship.screen.window.blit(self.get_current_pic(), self.get_xy())
        if Const.DEBUG:
            pygame.draw.rect(self.spaceship.screen.window, (255, 0, 0), self.hitbox, 1)
