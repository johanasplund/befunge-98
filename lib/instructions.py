import initialize as ini
import field_and_pointer as fp
import random
import re
import inputbox


def pop(stack):
    '''
    A modified pop function to match the properties of the stack in Befunge.
    If an empty stack is popped, the value 0 is returned.
    Else it uses stack.pop().
    '''
    return 0 if not stack else stack.pop()


def do_instruction(character):
    '''
    This function takes a character as input, and exectues the
    corresponding instruction in Befunge.
    '''
    for n in range(ini.pointer.maxiters_k):
        if all([not ini.pointer.read,
                not ini.pointer.do_nothing,
                not ini.pointer.read_once]):
            if character == ">":
                ini.pointer.direction = "right"
            elif character == "v":
                ini.pointer.direction = "down"
            elif character == "<":
                ini.pointer.direction = "left"
            elif character == "^":
                ini.pointer.direction = "up"
            elif character == "?":
                ini.pointer.direction = random.choice(
                    ["right", "down", "up", "left"])
            elif character == "@":
                ini.pointer.stop()
            elif re.match("[0-9]", character):
                ini.stackstack[-1].append(int(character))
            elif re.match("[a-f]", character):
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
                outint = str(pop(ini.stackstack[-1]))
                out = ini.ini.stackfont.render(outint, 1,
                                               ini.STACK_OUTPUT_COLOR)
                ini.outsurf.blit(
                    out, (ini.STACKCHAR_WIDTH * ini.outcount,
                          ini.STACKCHAR_HEIGHT * ini.outline))
                ini.outcount += len(outint)
            elif character == ",":
                outtext = fp.chhr(pop(ini.stackstack[-1]))
                if outtext == "\n":
                    ini.outline += 1
                    ini.outcount = -1
                    out = ini.stackfont.render("", 1, ini.STACK_OUTPUT_COLOR)
                else:
                    out = ini.stackfont.render(outtext, 1,
                                               ini.STACK_OUTPUT_COLOR)
                ini.outsurf.blit(out,
                                 (ini.STACKCHAR_WIDTH * ini.outcount,
                                  ini.STACKCHAR_HEIGHT * ini.outline))
                ini.outcount += len(outtext)
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
            elif re.match("[\[\]]", character):
                dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
                current_index = dirs.index(ini.pointer.direction)
                if character == "[":
                    ini.pointer.direction = dirs[(current_index - 1) % 4]
                elif character == "]":
                    ini.pointer.direction = dirs[(current_index + 1) % 4]
            elif character == "s":
                write_next = pop(ini.stackstack[-1])
                ini.the_field.put_char(
                    ini.pointer.xy[1] + ini.pointer.direction[1],
                    ini.pointer.xy[0] + ini.pointer.direction[0],
                    write_next)
                ini.pointer.step()
            elif character == "w":
                a = pop(ini.stackstack[-1])
                b = pop(ini.stackstack[-1])
                if b > a:
                    ini.pointer.direction = dirs[(current_index + 1) % 4]
                elif a > b:
                    ini.pointer.direction = dirs[(current_index - 1) % 4]
            elif character == "n":
                ini.stackstack[-1] = []
            elif character == "x":
                dy = pop(ini.stackstack[-1])
                dx = pop(ini.stackstack[-1])
                ini.pointer.direction = (dx, dy)
            elif character == "k":
                maxiters = pop(ini.stackstack[-1])
                if not maxiters:
                    maxiters = 1
                    do_instruction("r")
                else:
                    ini.pointer.step()
                    do_instruction(ini.pointer.current_char())
            elif character == "{":
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
            elif character == "}":
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
            elif character == "u":
                if len(ini.stackstack) == 1:
                    do_instruction("r")
                else:
                    count = pop(ini.stackstack[-1])
                    transfer = []
                    # SOSS -> TOSS if count > 0 else TOSS -> SOSS
                    sgn = lambda x: int(x / abs(x))
                    from_index = int((-3 - sgn(count)) / 2)
                    to_index = int((-3 + sgn(count)) / 2)
                    for n in range(abs(count)):
                        transfer.append(pop(ini.stackstack[from_index]))
                    for t in transfer:
                        ini.stackstack[to_index].append(t)

            elif character == "&":
                try:
                    ini.stackstack[-1].append(
                        int(inputbox.ask(ini.screen,
                            "Push a number to the stack")))
                except Exception:
                    return
            elif character == "~":
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
