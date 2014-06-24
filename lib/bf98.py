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
    codefont = pygame.font.Font("../font/Inconsolata.otf", 24)
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
            codechar = codefont.render(char, 1, charcolor)
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
    Blits all static visuals.
    '''
    render_code(ini.the_field.code)
    ini.screen.blit(ini.background, (0, 0))
    ini.screen.blit(ini.stacksurf, (0, ini.SCREEN_HEIGHT - 200))
    toss_text = ini.stackfont.render("TOSS", 1, ini.STACK_OUTPUT_COLOR)
    soss_text = ini.stackfont.render("SOSS", 1, ini.STACK_OUTPUT_COLOR)
    ini.stacksurf.blit(toss_text, (0, 0))
    ini.stacksurf.blit(soss_text, (ini.SCREEN_WIDTH / 4, 0))
    ini.screen.blit(ini.outsurf, (int(float(ini.SCREEN_WIDTH) / 2.0),
                    ini.SCREEN_HEIGHT - 200))
    ini.screen.blit(ini.pointer_rect, (ini.pointer.xy[0] * ini.CHAR_WIDTH,
                                       ini.pointer.xy[1] * ini.CHAR_HEIGHT))
    pygame.display.flip()


def run_code():
    '''
    This is the main method where the event loop is kept. This is where all
    the pygame magic is happening.
    '''
    paused = False
    step1 = False
    reset = False
    pygame.display.set_caption("Befunge-98 Interpreter")
    ini.background.fill(ini.BG_COLOR)
    ini.outsurf.fill((0, 0, 0, 100))
    ini.stacksurf.fill((0, 0, 0, 100))
    ini.pointer_rect.fill((255, 255, 255, 130))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_RIGHT:
                    step1 = not step1
                    paused = False
                elif event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_r:
                    reset = True
        if paused:
            continue
        if step1:
            paused = True
            step1 = False
        if reset:
            reset = False
            break
        initiate_new_run()
        ini.screen.blit(ini.background, (0, 0))
        ini.background.fill(ini.BG_COLOR)
        ini.screen.blit(ini.stacksurf, (0, ini.SCREEN_HEIGHT - 200))
        ini.screen.blit(
            ini.outsurf, (int(float(ini.SCREEN_WIDTH) / 2.0),
                          ini.SCREEN_HEIGHT - 200))
        ini.stacksurf.fill((0, 0, 0, 100))
        toss_text = ini.stackfont.render("TOSS", 1, ini.STACK_OUTPUT_COLOR)
        soss_text = ini.stackfont.render("SOSS", 1, ini.SOSS_OUTPUT_COLOR)
        ini.stacksurf.blit(toss_text, (0, 0))
        ini.stacksurf.blit(soss_text, (ini.SCREEN_WIDTH / 4, 0))
        ini.screen.blit(ini.pointer_rect,
                       (ini.pointer.xy[0] * ini.CHAR_WIDTH,
                        ini.pointer.xy[1] * ini.CHAR_HEIGHT))
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
    ini.the_field = fp.Field(fp.codelist)
    ini.pointer = fp.ini.Pointer((0, 0), (1, 0))
    ini.stackstack = [[]]
    run_code()

if __name__ == '__main__':
    pygame.init()
    run_code()
    pygame.quit()
