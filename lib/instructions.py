import initialize as ini
import field_and_pointer as fp
import random
import inputbox


def pop(stack):
    '''
    A modified pop function to match the properties of the stack in Befunge.
    If an empty stack is popped, the value 0 is returned,
    else it uses stack.pop().
    '''
    return 0 if not stack else stack.pop()


def new_block():
    '''
    Execution of the { instruction
    '''
    # Pop n
    transfer_amount = pop(ini.stackstack[-1])
    transfer = []
    # New TOSS
    ini.stackstack.append([])
    # Pop n elements
    if transfer_amount >= 0:
        for n in range(transfer_amount):
            transfer.append(pop(ini.stackstack[-2]))
    elif transfer_amount < 0:
        for n in range(-transfer_amount):
            transfer.append(0)
    # Push transfer elements
    for t in transfer[::-1]:
        ini.stackstack[-1].append(t)
    # Get storage offset
    stor_off = ini.the_field.storage_offset
    # Push storage offset to SOSS
    ini.stackstack[-2].append(stor_off[0])
    ini.stackstack[-2].append(stor_off[1])
    # Get new storage offset
    ini.the_field.storage_offset = (ini.pointer.xy[0] +
                                    ini.pointer.direction[0],
                                    ini.pointer.xy[1] +
                                    ini.pointer.direction[1])


def end_block():
    '''
    Execution of the } instruction
    '''
    # If ini.stackstack underflow
    if len(ini.stackstack) == 1:
        do_instruction("r")
    else:
        # Pop n
        transfer_amount = pop(ini.stackstack[-1])
        # Change storage offset to the top vector in SOSS
        ini.the_field.storage_offset = (pop(ini.stackstack[-2]),
                                        pop(ini.stackstack[-2]))
        # Transfers elements from TOSS to SOSS
        transfer = []
        if transfer_amount >= 0:
            for n in range(transfer_amount):
                transfer.append(pop(ini.stackstack[-1]))
        elif transfer_amount < 0:
            for n in range(-transfer_amount):
                pop(ini.stackstack[-2])
        # Push transfer elements
        for t in transfer[::-1]:
            ini.stackstack[-2].append(t)
        # Pop ini.stackstack[-1]
        pop(ini.stackstack)


def read_string():
    '''
    Execution of the ~ instruction
    '''
    if not ini.instring:
        ini.instring = list(
            inputbox.ask(ini.screen, "Push a string to the stack"))
        ini.instring.append(-1)
        ini.instring = ini.instring[::-1]
        ini.stackstack[-1].append(ord(ini.instring.pop()))
    else:
        if ini.instring[len(ini.instring) - 1] == -1:
            ini.stackstack[-1].append(int(ini.instring.pop()))
        else:
            ini.stackstack[-1].append(ord(ini.instring.pop()))


def read_int():
    '''
    Execution of the & instruction
    '''
    try:
        ini.stackstack[-1].append(
            int(inputbox.ask(ini.screen,
                "Push a number to the stack")))
    except Exception:
        return


def output_ascii():
    outtext = fp.chhr(pop(ini.stackstack[-1]))
    if outtext == "\n":
        ini._outline += 1
        ini._outcount = -1
        out = ini.stackfont.render("", 1, ini.STACK_OUTPUT_COLOR)
    else:
        out = ini.stackfont.render(outtext, 1,
                                   ini.STACK_OUTPUT_COLOR)
    ini.outsurf.blit(
        out, (ini.STACK_CHAR_WIDTH * ini._outcount,
              ini.STACK_CHAR_HEIGHT * ini._outline))
    ini._outcount += len(outtext)


def output_int():
    outint = str(pop(ini.stackstack[-1]))
    out = ini.stackfont.render(outint, 1, ini.STACK_OUTPUT_COLOR)
    ini.outsurf.blit(
        out, (ini.STACK_CHAR_WIDTH * ini._outcount,
              ini.STACK_CHAR_HEIGHT * ini._outline))
    ini._outcount += len(outint)


def do_instruction(character):
    '''
    This function takes a character as input, and exectues the
    corresponding instruction in Befunge.
    '''
    dir_dic = {">": "right", "v": "down", "<": "left", "^": "up"}
    dir_tuples = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    sgn = lambda x: int(x // abs(x)) if abs(x) else 0
    for n in range(ini.pointer.maxiters_k):
        if all([not ini.pointer.read,
                not ini.pointer.do_nothing,
                not ini.pointer.read_once]):
            if character in dir_dic:
                ini.pointer.direction = dir_dic[character]
            elif character == "?":
                ini.pointer.direction = random.choice(
                    ["right", "down", "up", "left"])
            elif character == "@":
                ini.pointer.stop()
            elif character in "0123456789":
                ini.stackstack[-1].append(int(character))
            elif character in "abcdef":
                ini.stackstack[-1].append(int(character, 16))
            elif character in ini.operators:
                ini.operators[character](pop(ini.stackstack[-1]),
                                         pop(ini.stackstack[-1]))
            elif character == "!":
                ini.stackstack[-1].append(1 if pop(ini.stackstack[-1]) == 0
                                          else 0)
            elif character == "$":
                pop(ini.stackstack[-1])
            elif character == "_":
                if pop(ini.stackstack[-1]) == 0:
                    ini.pointer.direction = "right"
                else:
                    ini.pointer.direction = "left"
            elif character == "|":
                if pop(ini.stackstack[-1]) == 0:
                    ini.pointer.direction = "down"
                else:
                    ini.pointer.direction = "up"
            elif character == ".":
                output_int()
            elif character == ",":
                output_ascii()
            elif character == ":":
                ini.stackstack[-1].extend([pop(ini.stackstack[-1])] * 2)
            elif character == "#":
                ini.pointer.step()
            elif character == "j":
                steps = pop(ini.stackstack[-1])
                for x in range(steps):
                    ini.pointer.step()
            elif character == "\"":
                ini.pointer.read = True
            elif character == "'":
                ini.pointer.read_once = True
            elif character == ";":
                ini.pointer.do_nothing = True
            elif character == "p":
                ini.the_field.put_char(pop(ini.stackstack[-1]),
                                       pop(ini.stackstack[-1]),
                                       pop(ini.stackstack[-1]))
            elif character == "r":
                ini.pointer.direction = (ini.pointer.direction[0] * -1,
                                         ini.pointer.direction[1] * -1)
            elif character in "[]":
                current_index = dir_tuples.index(ini.pointer.direction)
                if character == "[":
                    ini.pointer.direction = dir_tuples[(current_index - 1) % 4]
                elif character == "]":
                    ini.pointer.direction = dir_tuples[(current_index + 1) % 4]
            elif character == "s":
                ini.the_field.put_char(
                    ini.pointer.xy[1] + ini.pointer.direction[1],
                    ini.pointer.xy[0] + ini.pointer.direction[0],
                    pop(ini.stackstack[-1]))
                ini.pointer.step()
            elif character == "w":
                a = pop(ini.stackstack[-1])
                b = pop(ini.stackstack[-1])
                current_index = dir_tuples.index(ini.pointer.direction)
                ini.pointer.direction = dir_tuples[(current_index +
                                                   sgn((b > a) - (a > b))) % 4]
            elif character == "n":
                ini.stackstack[-1] = []
            elif character == "x":
                dy = pop(ini.stackstack[-1])
                dx = pop(ini.stackstack[-1])
                ini.pointer.direction = (dx, dy)
            elif character == "k":
                ini.pointer.maxiters_k = pop(ini.stackstack[-1])
                if not ini.pointer.maxiters_k:
                    ini.pointer.maxiters_k = 1
                    do_instruction("r")
                else:
                    ini.pointer.step()
                    do_instruction(ini.pointer.current_char())
            elif character == "{":
                new_block()
            elif character == "}":
                end_block()
            elif character == "u":
                if len(ini.stackstack) == 1:
                    do_instruction("r")
                else:
                    count = pop(ini.stackstack[-1])
                    transfer = []
                    # SOSS -> TOSS if count > 0 else TOSS -> SOSS
                    from_index = int((-3 - sgn(count)) / 2)
                    to_index = int((-3 + sgn(count)) / 2)
                    for n in range(abs(count)):
                        transfer.append(pop(ini.stackstack[from_index]))
                    for t in transfer:
                        ini.stackstack[to_index].append(t)

            elif character == "&":
                read_int()
            elif character == "~":
                read_string()
        elif character == "\"":
            ini.pointer.read = False
            ini.pointer.read_space = True
        elif character == ";":
            ini.pointer.do_nothing = False
        elif ini.pointer.read or ini.pointer.read_once:
            ini.pointer.read_once = False
            read_char = ord(character)
            if read_char == 32 and ini.pointer.read_space:
                ini.pointer.read_space = False
                ini.stackstack[-1].append(read_char)
            elif read_char != 32:
                ini.stackstack[-1].append(read_char)
        if ini.pointer.maxiters_k == 1:
            ini.pointer.step()
    ini.pointer.maxiters_k = 1
