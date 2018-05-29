#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PSYchology Python by Shi Yu
AXB experiment support functions
"""

# Todo :
#

__author__ = 'ShY'
__copyright__ = 'Copyright 2018, SHY'
__version__ = '0.1.0 (20180529)'
__maintainer__ = 'ShY, Pierre Halle'
__email__ = 'shi4yu2@gmail.com'
__status__ = 'Development'


from libpsypsy.psypsyinterface import *


# PyGame Environment =========================================
def initialisation_pygame(background):
    # Initialisation pyGame ==================================
    pygame.init()
    pygame.mixer.init()
    screen, scr_width, scr_height = setup_screen(background)

    # Fill background (gray)
    screen.fill(background)
    pygame.display.flip()
    return screen, scr_width, scr_height


def axb_pause(screen, screen_width, screen_height, background, instruction):
    screen.fill(background)
    pygame.display.flip()
    display_instruction(instruction, screen, screen_width, screen_height, background)
    return


# *=*=*=*=*=*=*=*= Display =*=*=*=*=*=*=*=*=*
# *=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
def get_screensize():
    # type: () -> (int, int)
    """
    Get the resolution of the screen
    :returns: width and height of the screen
    :rtype: tuple of int
    """
    infobject = pygame.display.Info()
    width = infobject.current_w
    height = infobject.current_h
    return width, height


def setup_screen(background=(150, 150, 150)):
    # type: (tuple) -> object
    """
    Get the resolution of the screen
    :param background: triple value of background (RGB)
    :type background: tuple
    :returns: window: pyGame Surface
    :rtype: Surface
    """
    background_list = list(background)
    (width, height) = get_screensize()
    window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    window.fill(background_list)
    # Deactivate mouse
    pygame.mouse.set_visible(False)
    pygame.display.flip()
    return [window, width, height]


# Sounds =====================================================
def mix_sound_stimuli(sound_path):
    """
    :param sound_path: list of path of sound files
    :type: sound_path: list[str]
    :return: mixed_sounds: list of pygame sound objects
    :rtype: mixed_sounds: list[Objects]
    :return: duration_sounds: list of durations
    rtype: duration_sounds: list[int]
    """
    mixed_sounds = []
    duration_sounds = []
    for i in sound_path:
        sound = pygame.mixer.Sound(i)
        mixed_sounds.append(sound)

        duration = int(round(pygame.mixer.Sound.get_length(sound), 3) * 1000)
        # 3 = duration in milliseconds
        duration_sounds.append(duration)

    return mixed_sounds, duration_sounds
