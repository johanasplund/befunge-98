#!/usr/bin/python
import pygame
import sys
import field_and_pointer as fp
import instructions as i
import initialize as ini


def render_code(code):
    '''
    Renders each character in the code with a specific syntax highlighing
    and blits the code to the background surface.
    '''
    for y, c in enumerate(code):
        for x, char in enumerate(c):
            if char in "0123456789abcdef":
                charcolor = (152, 152, 152)
            elif char in "+-*/%!`wk()":
                charcolor = (255, 136, 136)
            elif char in "><^v?_|#@jx[]r":
                charcolor = (136, 255, 136)
            elif char in ":\\$n":
                charcolor = (255, 255, 136)
            elif char in ".,&~":
                charcolor = (136, 255, 255)
            elif char in "\"\';":
                charcolor = (255, 136, 255)
            elif char in "{}upgsyt":
                charcolor = (136, 136, 255)
            else:
                charcolor = (206, 206, 206)
            codechar = ini.codefont.render(char, 1, charcolor)
            ini.background.blit(codechar, (ini.CHAR_WIDTH * x,
                                           ini.CHAR_HEIGHT * y))


def print_stack(stack, color, SOSS=False):
    '''
    Blits the TOSS and SOSS to the stack surface.
    '''
    for x, s in enumerate(stack[::-1]):
        try:
            printstack = ini.stackfont.render(
                "{}. {} [{}] ({})".format(x + 1, s,
                                          hex(s),
                                          fp.chhr(s)), 1, color)
        except Exception:
            printstack = ini.stackfont.render(
                "{}. {} ({})".format(x + 1, s, fp.chhr(s)), 1, color)
        if SOSS:
            ini.stacksurf.blit(printstack, (ini.SCREEN_WIDTH/4,
                                            ini.STACK_CHAR_HEIGHT * x + 20))
        else:
            ini.stacksurf.blit(printstack, (0, ini.STACK_CHAR_HEIGHT * x + 20))


def initiate_new_run():
    '''
    Blits all visuals.
    '''
    # Background, stack and output surfaces
    ini.screen.blit(ini.background, (0, 0))
    ini.screen.blit(ini.stacksurf, (0, ini.SCREEN_HEIGHT -
                                    ini.SCREEN_HEIGHT_MODIFIER))
    ini.screen.blit(ini.outsurf, (int(float(ini.SCREEN_WIDTH) / 2.0),
                    ini.SCREEN_HEIGHT -
                    ini.SCREEN_HEIGHT_MODIFIER))
    # Stack titles
    toss_text = ini.stackfont.render("TOSS", 1, ini.STACK_OUTPUT_COLOR)
    soss_text = ini.stackfont.render("SOSS", 1, ini.SOSS_OUTPUT_COLOR)
    ini.stacksurf.blit(toss_text, (0, 0))
    ini.stacksurf.blit(soss_text, (ini.SCREEN_WIDTH / 4, 0))
    # Pointer rectangle
    ini.screen.blit(ini.pointer_rect, (ini.pointer.xy[0] * ini.CHAR_WIDTH,
                                       ini.pointer.xy[1] * ini.CHAR_HEIGHT))
    pygame.display.flip()


def blit_statics():
    '''
    Blits all static visuals. This is to prevent the code
    and stack blits to pile up on top of each other.
    '''
    # Reset colors
    ini.background.fill(ini.BG_COLOR)
    ini.stacksurf.fill(ini.STACK_BG_COLOR)
    # Blit surfaces to screen
    ini.screen.blit(ini.background, (0, 0))
    ini.screen.blit(ini.stacksurf, (0, ini.SCREEN_HEIGHT -
                                    ini.SCREEN_HEIGHT_MODIFIER))
    ini.screen.blit(
        ini.outsurf, (int(float(ini.SCREEN_WIDTH) / 2.0),
                      ini.SCREEN_HEIGHT -
                      ini.SCREEN_HEIGHT_MODIFIER))
    # Stack titles
    toss_text = ini.stackfont.render("TOSS", 1, ini.STACK_OUTPUT_COLOR)
    soss_text = ini.stackfont.render("SOSS", 1, ini.SOSS_OUTPUT_COLOR)
    ini.stacksurf.blit(toss_text, (0, 0))
    ini.stacksurf.blit(soss_text, (ini.SCREEN_WIDTH / 4, 0))
    # Pointer rectangle
    ini.screen.blit(ini.pointer_rect,
                    (ini.pointer.xy[0] * ini.CHAR_WIDTH,
                     ini.pointer.xy[1] * ini.CHAR_HEIGHT))
    # The code
    render_code(ini.the_field.code)


def event_handler(pygame_event):
    for event in pygame_event:
        if event.type == pygame.QUIT:
            return "Quit"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ini._paused = not ini._paused
            elif event.key == pygame.K_RIGHT:
                ini._step_once = not ini._step_once
                ini._paused = False
            elif event.key == pygame.K_ESCAPE:
                return "Quit"
            elif event.key == pygame.K_r:
                ini._reset = True


def run_code():
    '''
    This is the main method where the event loop is kept. This is where all
    the pygame magic is happening.
    '''
    while True:
        get_event = event_handler(pygame.event.get())
        if get_event == "Quit":
            return
        if ini._paused:
            continue
        if ini._step_once:
            ini._paused = True
            ini._step_once = False
        if ini._reset:
            ini._reset = False
            break
        initiate_new_run()
        blit_statics()
        i.do_instruction(ini.pointer.current_char())
        # Print stack (TOSS)
        print_stack(ini.stackstack[-1], ini.STACK_OUTPUT_COLOR)
        # Print SOSS if it exists
        if len(ini.stackstack) >= 2:
            print_stack(ini.stackstack[-2], ini.SOSS_OUTPUT_COLOR, SOSS=True)
        try:
            pygame.time.wait(int(sys.argv[2]))
        except Exception:
            pygame.time.wait(50)
    # Reinitiating the code, pointer and stackstack
    ini.the_field = fp.Field(fp.codelist)
    ini.pointer = fp.ini.Pointer((0, 0), (1, 0))
    ini.stackstack = [[]]
    run_code()

if __name__ == '__main__':
    pygame.init()
    run_code()
    pygame.quit()
