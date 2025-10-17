import pygame
from const import Const
from time import perf_counter as clock


class Projectile:
    """
    Enemy projectile that falls downward and can hit the player's spaceship
    """

    def __init__(self, x, y):
        self.x = x - Const.PROJECTILE_WIDTH / 2  # Center it
        self.y = y
        self.speed = Const.PROJECTILE_SPEED
        self.width = Const.PROJECTILE_WIDTH
        self.height = Const.PROJECTILE_HEIGHT
        self.color = Const.PROJECTILE_COLOR
        self.core_color = Const.PROJECTILE_CORE_COLOR
        self.away = False
        self.hit = False
        self.exploding = False
        self.explosion_frame = 0
        self.explosion_time = 0
        self.hitbox = None
        self.update_hitbox()

    def update_hitbox(self):
        """Update the projectile's hitbox"""
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def destroy(self):
        """Trigger explosion animation"""
        self.hit = True
        self.exploding = True
        self.explosion_time = clock()

    def is_hit(self):
        """Check if projectile was hit"""
        return self.hit

    def move(self):
        """Move the projectile downward"""
        if not self.exploding:
            self.y += self.speed
            self.update_hitbox()

            # Remove if it goes off screen
            if self.y > Const.SCREEN_HEIGHT:
                self.away = True
        else:
            # Handle explosion animation
            if clock() - self.explosion_time > 0.1:  # Short explosion
                self.away = True

    def is_away(self):
        """Check if the projectile should be removed"""
        return self.away

    def get_xy(self):
        """Return the position"""
        return self.x, self.y

    def draw(self, screen):
        """Draw the projectile with a pixelated retro look"""
        if self.exploding:
            # Draw simple explosion effect (expanding circle)
            radius = int(8 * (clock() - self.explosion_time) / 0.1)
            pygame.draw.circle(screen, (255, 150, 0),
                             (int(self.x + self.width/2), int(self.y + self.height/2)),
                             radius)
        else:
            # Draw pixelated projectile shape (like a classic laser bolt)
            # Outer pixels
            pygame.draw.rect(screen, self.color, self.hitbox)

            # Inner bright core (2 pixels narrower on each side)
            core_rect = pygame.Rect(self.x + 2, self.y + 2, self.width - 4, self.height - 4)
            pygame.draw.rect(screen, self.core_color, core_rect)

            # Top and bottom pixels for shape
            tip_width = max(2, self.width - 4)
            top_rect = pygame.Rect(self.x + (self.width - tip_width)/2, self.y, tip_width, 2)
            bottom_rect = pygame.Rect(self.x + (self.width - tip_width)/2,
                                     self.y + self.height - 2, tip_width, 2)
            pygame.draw.rect(screen, self.core_color, top_rect)
            pygame.draw.rect(screen, self.core_color, bottom_rect)

        if Const.DEBUG:
            pygame.draw.rect(screen, (255, 255, 0), self.hitbox, 1)
