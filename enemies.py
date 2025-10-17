from asteroid import Asteroid
from invader import Invader
from projectile import Projectile
from random import randint, uniform
from const import Const
from resources import Resources
from direction import Direction
import pygame


class Enemies:
    """
    Two types of enemies in this game:
        * Asteroids are random and annoying, but sometimes when you're lucky
          they help blow up more than one invader with a single rocket
        * Invaders are the ugly enemies from outer space, destroy them or be
          destroyed
    """

    def __init__(self, game):
        self.game = game
        self.asteroids = []
        self.invaders = []
        self.projectiles = []

    def get_enemies(self):
        """
        Return all enemies
        """
        return self.asteroids + self.invaders

    def add_asteroid(self):
        """
        Add a new asteroid with random values
        """
        speed_vertical = uniform(Const.ASTEROID_SPEED_VERTICAL_MIN, Const.ASTEROID_SPEED_VERTICAL_MAX)
        speed_horizontal = uniform(Const.ASTEROID_SPEED_HORIZONTAL_MIN, Const.ASTEROID_SPEED_HORIZONTAL_MAX)
        acc_vertical = uniform(Const.ASTEROID_ACCELERATION_VERTICAL_MIN, Const.ASTEROID_ACCELERATION_VERTICAL_MAX)
        acc_horizontal = uniform(Const.ASTEROID_ACCELERATION_HORIZONTAL_MIN, Const.ASTEROID_ACCELERATION_HORIZONTAL_MAX)
        x = randint(Const.ASTEROID_BORDER_LEFT, Const.ASTEROID_BORDER_RIGHT)
        y = Const.ASTEROID_APPEAR_HEIGHT
        asteroid = Asteroid(
            images=Resources.asteroid1,
            speed=(speed_horizontal, speed_vertical),
            acceleration=(acc_horizontal, acc_vertical),
            x=x,
            y=y
        )
        self.asteroids.append(asteroid)

    def add_invader(self, x, y, speed):
        """
        Add an invader to enemies, converting the provided parameters
        """
        invader = Invader(images=Resources.invader1,
                          x=x, y=y,
                          descend_speed=speed,
                          horizontal_speed=speed,
                          descend_steps=20)
        self.invaders.append(invader)

    def invaders_arrived(self):
        """
        The invaders have reached their nominal height
        """
        if randint(0, 1) == 0:
            direction = Direction.right
        else:
            direction = Direction.left
        for invader in self.invaders:
            invader.arrived(direction)

    def all_invaders_appeared(self):
        """
        Check if all invaders already appear on the screen
        """
        for invader in self.invaders:
            if invader.get_xy()[1] < Const.INVADER_TOP_BORDER:
                return False
        return True

    def current_number_of_invaders(self):
        """
        Return the remaining number of invaders
        """
        return len(self.invaders)

    def get_projectiles(self):
        """
        Return all enemy projectiles
        """
        return self.projectiles

    def invader_shoot(self):
        """
        Randomly select an invader to shoot a projectile
        """
        # Only shoot if there are invaders that can shoot
        shooting_invaders = [inv for inv in self.invaders if inv.can_shoot and not inv.is_hit()]
        if shooting_invaders:
            shooter = shooting_invaders[randint(0, len(shooting_invaders) - 1)]
            x, y = shooter.get_projectile_spawn_position()
            self.projectiles.append(Projectile(x, y))

    def move(self):
        """
        Move all existing enemies
        """
        enemies = self.get_enemies()
        to_remove = []
        direction_swap_needed = False
        # Move all the enemies
        for enemy in enemies:
            enemy.move()
            # Check if the enemy is off the screen, it should be removed
            if enemy.is_away():
                to_remove.append(enemy)
            # Check if we need to change the direction of the invaders
            if isinstance(enemy, Invader):
                horizontal_location, _ = enemy.get_xy()
                direction = enemy.get_horizontal_direction()
                if horizontal_location >= Const.INVADER_RIGHT_BORDER and direction == Direction.right or \
                        horizontal_location <= Const.INVADER_LEFT_BORDER and direction == Direction.left:
                    direction_swap_needed = True
            # This will blow up other enemies within reach
            if enemy.is_hit():
                for other_enemy in enemies:
                    if not other_enemy.is_hit() and pygame.Rect(enemy.hitbox).colliderect(other_enemy.hitbox):
                        other_enemy.hit()
                        self.game.add_score(other_enemy)
        # At least one invader has crossed the side border, and all reverse direction
        if direction_swap_needed:
            for invader in self.invaders:
                invader.descend()
                invader.swap_direction()
        # If some enemies have moved off the screen, they must be removed
        for enemy in to_remove:
            if isinstance(enemy, Asteroid):
                self.asteroids.remove(enemy)
            elif isinstance(enemy, Invader):
                self.invaders.remove(enemy)

        # Move projectiles
        projectiles_to_remove = []
        for projectile in self.projectiles:
            projectile.move()
            if projectile.is_away():
                projectiles_to_remove.append(projectile)
        for projectile in projectiles_to_remove:
            self.projectiles.remove(projectile)

    def draw(self):
        """
        Draw all existing enemies
        """
        for asteroid in self.asteroids:
            self.game.screen.window.blit(asteroid.get_current_pic(), asteroid.get_xy())
            if Const.DEBUG:
                pygame.draw.rect(self.game.screen.window, (255, 255, 0), asteroid.get_hitbox(), 1)
        for invader in self.invaders:
            self.game.screen.window.blit(invader.get_current_pic(), invader.get_xy())
            if Const.DEBUG:
                pygame.draw.rect(self.game.screen.window, (255, 0, 0), invader.get_hitbox(), 1)
        for projectile in self.projectiles:
            projectile.draw(self.game.screen.window)
