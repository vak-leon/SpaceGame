class Level:

    __level_number = 0

    @staticmethod
    def new_level():
        current_level = Level.__level_number
        Level.__level_number += 1
        return current_level

    def __init__(self):
        self.level_number = Level.new_level()
        self.invaders_locations = []
        self.num_of_invaders = 0
        self.asteroids_probability = 0
        self.shooting_probability = 0

    def set_invader_locations(self, locations):
        self.invaders_locations = locations

    def get_invader_locations(self):
        return self.invaders_locations

    def get_level_number(self):
        return self.level_number

    def set_num_of_invaders(self, num):
        self.num_of_invaders = num

    def get_num_of_invaders(self):
        return self.num_of_invaders

    def set_asteroids_probability(self, probability):
        self.asteroids_probability = probability

    def get_asteroids_probability(self):
        return self.asteroids_probability

    def set_shooting_probability(self, probability):
        self.shooting_probability = probability

    def get_shooting_probability(self):
        return self.shooting_probability
