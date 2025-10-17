from enemy import Enemy
from time import perf_counter as clock
from const import Const


class Invader(Enemy):
    def __init__(self, images, x, y,
                 descend_speed, horizontal_speed, descend_steps):
        super().__init__(images=images, speed=(0, 0), x=x, y=y)
        self.next_frame = 0
        self.frame_num = 0
        self.frame_direction = 1
        self.exploding = False
        self.frame_time = Const.EXPLOSION_ANIMATE_SPEED
        self.images = self.rescale(images_source=self.original_images,
                                   scale_x=Const.INVADER_SIZE,
                                   scale_y=Const.INVADER_SIZE)  # Square invader
        self.num_of_images = len(self.images) - 1
        self.current_image_set = self.images
        self.width, self.height = self.images[0].get_rect().size
        self.hitsize = tuple(map(sum, zip((0, 0, self.width, self.height), Const.INVADER_HITSIZE)))
        self.descend_steps = descend_steps
        self.descend_step = 0
        self.descend_speed = descend_speed
        self.horizontal_speed = horizontal_speed
        self.descend_finished = True
        self.entry_finished = False
        self.speed = (0, Const.INVADER_ENTRY_SPEED)
        self.allow_off_the_screen = True
        self.score = 100
        self.can_shoot = False  # Only shoot after entry is finished

    def set_speed(self, speed):
        """
        Set invader speed (tuple)
        """
        self.speed = speed

    def move_aside(self, direction):
        """
        Horizontal invader movement
        """
        self.horizontal_speed *= direction.value
        self.speed = (self.horizontal_speed, 0)

    def swap_direction(self):
        """
        Start moving to the other horizontal direction
        """
        self.horizontal_speed = -self.horizontal_speed

    def descend(self):
        """
        Invader will begin descent, i.e. moving down
        """
        self.descend_step = 0
        self.descend_finished = False
        self.speed = (0, self.descend_speed)

    def get_descend_finished(self):
        """
        Return whether the descend has finished
        """
        return self.descend_finished

    def arrived(self, direction):
        """
        Command the invader that it arrived to the starting position on the screen
        """
        self.entry_finished = True
        self.allow_off_the_screen = False
        self.can_shoot = True  # Enable shooting once in position
        self.move_aside(direction)

    def get_projectile_spawn_position(self):
        """
        Return the position where a projectile should spawn (center bottom of invader)
        """
        center_x = self.x + self.width / 2
        bottom_y = self.y + self.height
        return center_x, bottom_y

    def move(self):
        """
        Move the invader according to its direction and state
        """
        if self.entry_finished:
            if not self.descend_finished:
                self.descend_step += 1
                if self.descend_step >= self.descend_steps:
                    self.descend_finished = True
                    self.speed = (self.horizontal_speed, 0)
        super().move()

    def get_current_pic(self):
        """
        Return the current image of the invader
        """
        if clock() > self.next_frame:
            if self.exploding:
                if self.frame_num < self.num_of_explosion_frames:
                    self.frame_num += 1
                else:
                    self.away = True
            else:
                self.frame_num += self.frame_direction
                if self.frame_num > self.num_of_images:
                    self.frame_direction = -self.frame_direction
                    # The last frame will be shown twice, for showing it once multiply the direction by 2 below.
                    self.frame_num += self.frame_direction
                elif self.frame_num < 0:
                    self.frame_direction = -self.frame_direction
                    # The first frame will be shown twice, for showing it once multiply the direction by 2 below.
                    self.frame_num += self.frame_direction
            self.next_frame = clock() + self.frame_time
        return self.current_image_set[self.frame_num]
