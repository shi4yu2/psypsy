"""
PSYchology Python by Shi Yu
Interface with Pygame
"""

# Todo :
#

__author__ = 'ShY'
__copyright__ = 'Copyright 2018, SHY'
__version__ = '0.1.0 (20180529)'
__maintainer__ = 'ShY, Pierre Halle'
__email__ = 'shi4yu2@gmail.com'
__status__ = 'Development'


import sys
import pygame
import pygame.font
import pygame.event
import pygame.draw
from pygame.locals import *


def wait_for_space():
    """
    Continue program when press SPACE
    Terminate program when press ESC
    """
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                return


# *=*=*=*=*=*=*=*= Display =*=*=*=*=*=*=*=*=*
# *=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
def clear_screen(screen, background=(150, 150, 150)):
    # type: (object, tuple) -> ()
    """
    Clear the current display surface
    :param screen: current display surface
    :type screen: Surface
    :param background: triple value of background (RGB)
    :type background: tuple
    """
    background_list = list(background)
    screen.fill(background_list)
    pygame.display.flip()
    pygame.event.pump()
    pygame.event.clear()  # clear event
    return


def point_fixation(screen, duration, fixation="+", font="helvetica", font_size=60):
    # type: (object, int, str, str, int) -> ()
    """
    display the point of fixation
    :param screen: current display surface
    :type screen: Surface
    :param duration: duration of the fixation point
    :type duration: int
    :param fixation: character of fixation
    :type fixation: str
    :param font: text font
    :type font: str
    :param font_size: text font size
    :type font: int
    """
    display_text(screen, fixation, font, font_size)
    pygame.display.flip()
    pygame.event.pump()
    pygame.event.clear()
    pygame.time.wait(duration)  # time of fixation point
    return


# *=*=*=*=*=*=*=*=*= Image =*=*=*=*=*=*=*=*=*
# *=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
def display_image(filename, screen, screen_width, screen_height):
    # type: (str, object, int, int) -> ()
    """
    Display an image centered on the screen
    :param filename: image filename
    :type filename: str
    :param screen: current display surface
    :type screen: Surface
    :param screen_width: current display width
    :type screen_width: int
    :param screen_height: current display height
    :type screen_height: int
    """
    image = pygame.image.load(filename)
    image2 = pygame.transform.scale(image, (screen_width, screen_height))
    screen.blit(image2, (0, 0))
    pygame.display.flip()
    pygame.event.pump()
    pygame.event.clear()
    return


def display_instruction(filename, screen, screen_width, screen_height, background):
    # type: (str, object, int, int, tuple) -> ()
    """
    Display an image centered on the screen
    :param filename: image filename
    :type filename: str
    :param screen: current display surface
    :type screen: Surface
    :param screen_width: current display width
    :type screen_width: int
    :param screen_height: current display height
    :type screen_height: int
    :param background: triple value of background (RGB)
    :type background: tuple
    """
    display_image(filename, screen, screen_width, screen_height)
    pygame.time.wait(1000)
    wait_for_space()
    clear_screen(screen, background)
    return


# *=*=*=*=*=*=*=*=*= Text  =*=*=*=*=*=*=*=*=*
# *=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
def display_text(screen, text, font="Cyberbit", font_size=60):
    # type: (object, str, str, int) -> ()
    """
    display text at the center of the current display surface
    :param screen: current display surface
    :type screen: Surface
    :param text: text to be displayed
    :type text: str
    :param font: text font
    :type font: str
    :param font_size: text font size
    :type font: int
    """
    my_font = pygame.font.SysFont(font, font_size)
    text_obj = my_font.render(text, True, (0, 0, 0))
    # center text
    text_position = text_obj.get_rect()
    text_position.centerx = screen.get_rect().centerx
    text_position.centery = screen.get_rect().centery
    screen.blit(text_obj, text_position)
    pygame.display.flip()
    pygame.event.pump()
    pygame.event.clear()
    return


def display_text_colour(screen, text, font="Cyberbit", font_size=60, colour=(255, 0, 0)):
    # type: (object, str, str, int, tuple) -> ()
    """
    display text at the center of the current display surface
    :param screen: current display surface
    :type screen: Surface
    :param text: text to be displayed
    :type text: str
    :param font: text font
    :type font: str
    :param font_size: text font size
    :type font_size: int
    :param colour: text font colour
    :type colour: tuple
    """
    my_font = pygame.font.SysFont(font, font_size)
    text_obj = my_font.render(text, True, colour)
    # center text
    text_position = text_obj.get_rect()
    text_position.centerx = screen.get_rect().centerx
    text_position.centery = screen.get_rect().centery
    screen.blit(text_obj, text_position)
    pygame.display.flip()
    pygame.event.pump()
    pygame.event.clear()
    return


def display_utf8text(screen, text, font_size=60):
    # type: (object, str, str, int) -> ()
    """
    display text at the center of the current display surface
    :param screen: current display surface
    :type screen: Surface
    :param text: text to be displayed
    :type text: str
    :param font_size: text font size
    :type font_size: int
    """
    # my_font = pygame.font.SysFont(font, font_size)
    my_font = pygame.font.Font("simsun.ttf", font_size)
    text_obj = my_font.render(text, True, (0, 0, 0))
    # center text
    text_position = text_obj.get_rect()
    text_position.centerx = screen.get_rect().centerx
    text_position.centery = screen.get_rect().centery
    screen.blit(text_obj, text_position)
    pygame.display.flip()
    pygame.event.pump()
    pygame.event.clear()
    return
