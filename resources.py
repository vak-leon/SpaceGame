import pygame


class Resources:

    ship_move_right = [pygame.image.load("res/spaceship_N_00.png"),
                       pygame.image.load("res/spaceship_R_01.png"),
                       pygame.image.load("res/spaceship_R_02.png"),
                       pygame.image.load("res/spaceship_R_03.png"),
                       pygame.image.load("res/spaceship_R_04.png"),
                       pygame.image.load("res/spaceship_R_05.png"),
                       pygame.image.load("res/spaceship_R_06.png")]

    ship_move_left = [pygame.image.load("res/spaceship_N_00.png"),
                      pygame.image.load("res/spaceship_L_01.png"),
                      pygame.image.load("res/spaceship_L_02.png"),
                      pygame.image.load("res/spaceship_L_03.png"),
                      pygame.image.load("res/spaceship_L_04.png"),
                      pygame.image.load("res/spaceship_L_05.png"),
                      pygame.image.load("res/spaceship_L_06.png")]

    rocket = [pygame.image.load("res/rocket_00.png"),
              pygame.image.load("res/rocket_01.png"),
              pygame.image.load("res/rocket_02.png"),
              pygame.image.load("res/rocket_03.png"),
              pygame.image.load("res/rocket_04.png"),
              pygame.image.load("res/rocket_05.png")]

    flame = [pygame.image.load("res/flame_01.png"),
             pygame.image.load("res/flame_02.png"),
             pygame.image.load("res/flame_03.png"),
             pygame.image.load("res/flame_04.png"),
             pygame.image.load("res/flame_05.png")]

    planets = [pygame.image.load("res/planet_01.png"),
               pygame.image.load("res/planet_02.png"),
               pygame.image.load("res/planet_03.png"),
               pygame.image.load("res/planet_04.png"),
               pygame.image.load("res/planet_05.png")]

    star_small = [pygame.image.load("res/star_1_01.png"),
                  pygame.image.load("res/star_1_02.png"),
                  pygame.image.load("res/star_1_03.png"),
                  pygame.image.load("res/star_1_04.png"),
                  pygame.image.load("res/star_1_05.png"),
                  pygame.image.load("res/star_1_06.png")]

    star_bright = [pygame.image.load("res/star_2_01.png"),
                   pygame.image.load("res/star_2_02.png"),
                   pygame.image.load("res/star_2_03.png"),
                   pygame.image.load("res/star_2_04.png"),
                   pygame.image.load("res/star_2_05.png"),
                   pygame.image.load("res/star_2_06.png")]

    explosion = [pygame.image.load("res/explosion_01.png"),
                 pygame.image.load("res/explosion_02.png"),
                 pygame.image.load("res/explosion_03.png"),
                 pygame.image.load("res/explosion_04.png"),
                 pygame.image.load("res/explosion_05.png")]

    asteroid1 = [pygame.image.load("res/asteroid_1_01.png"),
                 pygame.image.load("res/asteroid_1_02.png"),
                 pygame.image.load("res/asteroid_1_03.png"),
                 pygame.image.load("res/asteroid_1_04.png"),
                 pygame.image.load("res/asteroid_1_05.png"),
                 pygame.image.load("res/asteroid_1_06.png"),
                 pygame.image.load("res/asteroid_1_07.png"),
                 pygame.image.load("res/asteroid_1_08.png"),
                 pygame.image.load("res/asteroid_1_09.png"),
                 pygame.image.load("res/asteroid_1_10.png")]

    invader1 = [pygame.image.load("res/invader_00.png"),
                pygame.image.load("res/invader_01.png"),
                pygame.image.load("res/invader_02.png"),
                pygame.image.load("res/invader_03.png"),
                pygame.image.load("res/invader_04.png"),
                pygame.image.load("res/invader_05.png"),
                pygame.image.load("res/invader_06.png"),
                pygame.image.load("res/invader_07.png"),
                pygame.image.load("res/invader_08.png"),
                pygame.image.load("res/invader_09.png"),
                pygame.image.load("res/invader_10.png"),
                pygame.image.load("res/invader_11.png"),
                pygame.image.load("res/invader_12.png"),
                pygame.image.load("res/invader_13.png"),
                pygame.image.load("res/invader_14.png")]

    try:
        pygame.mixer.pre_init(44100, -16, 2, 1024)
        pygame.mixer.init()
        wav_launch = [pygame.mixer.Sound("res/launch.wav")]
        wav_explosion = [pygame.mixer.Sound("res/explosion_01.wav"),
                         pygame.mixer.Sound("res/explosion_02.wav")]
        audio_enabled = True
    except pygame.error:
        wav_launch = []
        wav_explosion = []
        audio_enabled = False
