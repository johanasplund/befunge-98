import pygame
import field_and_pointer as fp

# Stack, field, pointer and the 2-input operators
stackstack = [[]]
the_field = fp.Field(fp.load_code())
pointer = fp.Pointer((0, 0), (1, 0))
operators = {
    "+": lambda x1, x2: stackstack[-1].append(x1 + x2),
    "-": lambda x1, x2: stackstack[-1].append(x2 - x1),
    "*": lambda x1, x2: stackstack[-1].append(x1 * x2),
    "/": lambda x1, x2:
    stackstack[-1].append(int(float(x2) // float(x1)))
    if x1 else stackstack[-1].append(0),
    "%": lambda x1, x2: stackstack[-1].append(x2 % x1),
    "`": lambda x1, x2:
    stackstack[-1].append(1) if x2 > x1 else stackstack[-1].append(0),
    "\\": lambda x1, x2: stackstack[-1].extend([x1, x2]),
    "g": lambda x1, x2: stackstack[-1].append(ord(the_field.get_char(x2, x1)))}

# Global constants related to pygame
CHAR_WIDTH = 12
CHAR_HEIGHT = 28
SCREEN_HEIGHT = the_field.Y * CHAR_HEIGHT + 200
SCREEN_WIDTH = the_field.X * CHAR_WIDTH + 500
BG_COLOR = (52, 52, 52)
STACK_OUTPUT_COLOR = (230, 200, 70)
SOSS_OUTPUT_COLOR = (70, 230, 200)
STACK_CHAR_HEIGHT = 16
STACK_CHAR_WIDTH = 10

# Pygame surface inits
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.Surface(screen.get_size()).convert()
pointer_rect = pygame.Surface((CHAR_WIDTH, CHAR_HEIGHT), pygame.SRCALPHA)
stacksurf = pygame.Surface((SCREEN_WIDTH, 200), pygame.SRCALPHA)
outsurf = pygame.Surface((int(float(SCREEN_WIDTH) / 2.0), 200),
                         pygame.SRCALPHA)
pygame.font.init()
stackfont = pygame.font.Font("../font/Inconsolata.otf", 18)

# Global constants related to bf98.py
_outcount = 0
_outline = 0
_instring = ""
