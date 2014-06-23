#!/usr/bin/python
import pygame
import re
import random
import sys
from math import floor
import six
import inputbox


class Field(object):
	def __init__(self, code):
		super(Field, self).__init__()
		self.Y = len(code)
		self.X = max([len(code[l]) for l in range(self.Y)])
		self.code = []
		for c in code:
			if self.X > len(c):
				c += " "*(self.X-len(c))
			self.code.append(list(c))
		self.direction = (1, 0)
		self.xy = (0, 0)
		self.read = False
		self.read_once = False
		self.rest = False
		self.storage_offset = (0, 0)

	def step(self):
		self.xy = ((self.xy[0] + self.direction[0]) % self.X,
					(self.xy[1] + self.direction[1]) % self.Y)

	def change_direction(self, newdir):
		if newdir == "up":
			self.direction = (0, -1)
		elif newdir == "down":
			self.direction = (0, 1)
		elif newdir == "left":
			self.direction = (-1, 0)
		elif newdir == "right":
			self.direction = (1, 0)
		else:
			print("Invalid direction input")

	def change_direction_tuple(self, newdir):
		self.direction = newdir

	def stop(self):
		self.direction = (0, 0)

	def print_field(self, font):
		for c in self.code:
			print("".join(c))

	def current_char(self):
		return self.code[self.xy[1] % self.Y][self.xy[0] % self.X]

	def read_unichr(self, bl):
		self.read = bl

	def read_unichr_once(self, bl):
		self.read_once = bl

	def do_nothing(self, bl):
		self.rest = bl

	def get_char(self, xget, yget):
		return self.code[yget % self.Y][xget % self.X]

	def put_char(self, yput, xput, v):
		ynew = yput + self.storage_offset[1]
		xnew = xput + self.storage_offset[0]
		self.code[ynew % self.Y][xnew % self.X] = chhr(v)

	def change_storage_offset(self, x, y):
		self.storage_offset = (x, y)


def pop(stack):
	return 0 if not stack else stack.pop()


def chhr(tal):
	if tal <= 0:
		return " "
	else:
		return six.unichr(tal)


def sgn(nmbr):
	return int(nmbr/abs(nmbr))


def render_code(code):
	codefont = pygame.font.Font("./font/Inconsolata.otf", 24)
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
				background.blit(codechar, (CHARWIDTH*x, CHARHEIGHT*y))


global stackstack
global operations
global the_field
global background
global screen
global CHARWIDTH
global CHARHEIGHT
global BGCOLOR
global STACKOUTPUTCOLOR
global SOSSOUTPUTCOLOR
global cursor
global stacksurf
global outsurf
global stackfont
global outcount
global outline
global instring
global just_read
global maxiters
global read_space
pygame.init()
stackstack = [[]]
with open(sys.argv[1], "r") as c:
	codelist = c.read().splitlines()
the_field = Field(codelist)
ops = {"+": lambda x1, x2: stackstack[-1].append(x1 + x2),
		"-": lambda x1, x2: stackstack[-1].append(x2 - x1),
		"*": lambda x1, x2: stackstack[-1].append(x1 * x2),
		"/": lambda x1, x2: stackstack[-1].append(int(floor(float(x2)/float(x1)))),
		"%": lambda x1, x2: stackstack[-1].append(x2 % x1),
		"`": lambda x1, x2: stackstack[-1].append(1) if x2 > x1 else stackstack[-1].append(0),
		"\\": lambda x1, x2: stackstack[-1].extend([x1, x2]),
		"g": lambda x1, x2: stackstack[-1].append(ord(the_field.get_char(x2, x1)))}
CHARWIDTH = 12
CHARHEIGHT = 28
SCREENHEIGHT = the_field.Y*CHARHEIGHT+200
SCREENWIDTH = max(the_field.X*CHARWIDTH+500, 320)
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
background = pygame.Surface(screen.get_size()).convert()
cursor = pygame.Surface((CHARWIDTH, CHARHEIGHT), pygame.SRCALPHA)
stacksurf = pygame.Surface((SCREENWIDTH, 200), pygame.SRCALPHA)
outsurf = pygame.Surface((int(float(SCREENWIDTH)/2.0), 200), pygame.SRCALPHA)
stackfont = pygame.font.Font("./font/Inconsolata.otf", 18)
BGCOLOR = (52, 52, 52)
STACKOUTPUTCOLOR = (230, 200, 70)
SOSSOUTPUTCOLOR = (70, 230, 200)
STACKCHARHEIGHT = 16
STACKCHARWIDTH = 10
outcount = 0
outline = 0
instring = ""
just_read = False
read_space = True
maxiters = 1


def do_instruction(character):
	global stackstack
	global operations
	global the_field
	global background
	global screen
	global CHARWIDTH
	global CHARHEIGHT
	global BGCOLOR
	global STACKOUTPUTCOLOR
	global SOSSOUTPUTCOLOR
	global cursor
	global stacksurf
	global outsurf
	global stackfont
	global STACKCHARWIDTH
	global STACKCHARHEIGHT
	global outcount
	global outline
	global instring
	global just_read
	global maxiters
	global read_space
	for n in range(maxiters):
		if not the_field.read and not the_field.rest and not the_field.read_once:
			if character == ">":
				the_field.change_direction("right")
			elif character == "v":
				the_field.change_direction("down")
			elif character == "<":
				the_field.change_direction("left")
			elif character == "^":
				the_field.change_direction("up")
			elif character == "?":
				the_field.change_direction(random.choice(["right", "down", "up", "left"]))
			elif character == "@":
				the_field.stop()
			elif re.match("[0-9]", character):
				stackstack[-1].append(int(character))
			elif re.match("[a-f]", character):
				stackstack[-1].append(int(character, 16))
			elif character in ops:
				ops[character](pop(stackstack[-1]), pop(stackstack[-1]))
			elif character == "!":
				stackstack[-1].append(1 if pop(stackstack[-1]) == 0 else 0)
			elif character == "$":
				pop(stackstack[-1])
			elif character == "_":
				if pop(stackstack[-1]) == 0:
					the_field.change_direction("right")
				else:
					the_field.change_direction("left")
			elif character == "|":
				if pop(stackstack[-1]) == 0:
					the_field.change_direction("down")
				else:
					the_field.change_direction("up")
			elif character == ".":
				outint = str(pop(stackstack[-1]))
				out = stackfont.render(outint, 1, STACKOUTPUTCOLOR)
				outsurf.blit(out, (STACKCHARWIDTH*outcount, STACKCHARHEIGHT*outline))
				outcount += len(outint)
			elif character == ",":
				outtext = chhr(pop(stackstack[-1]))
				if outtext == "\n":
					outline += 1
					outcount = -1
					out = stackfont.render("", 1, STACKOUTPUTCOLOR)
				else:
					out = stackfont.render(outtext, 1, STACKOUTPUTCOLOR)
				outsurf.blit(out, (STACKCHARWIDTH*outcount, STACKCHARHEIGHT*outline))
				outcount += len(outtext)
			elif character == ":":
				stackstack[-1].extend([pop(stackstack[-1])]*2)
			elif character == "#":
				the_field.step()
			elif character == "j":
				steps = pop(stackstack[-1])
				for x in range(steps):
					the_field.step()
			elif character == "\"":
				the_field.read_unichr(True)
			elif character == "'":
				the_field.read_unichr_once(True)
				just_read = True
			elif character == ";":
				the_field.do_nothing(True)
			elif character == "p":
				the_field.put_char(pop(stackstack[-1]), pop(stackstack[-1]), pop(stackstack[-1]))
			elif character == "r":
				the_field.change_direction_tuple((the_field.direction[0] * -1,
												the_field.direction[1] * -1))
			elif re.match("[\[\]]", character):
				dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
				current_index = dirs.index(the_field.direction)
				if character == "[":
					the_field.change_direction_tuple(dirs[(current_index - 1) % 4])
				elif character == "]":
					the_field.change_direction_tuple(dirs[(current_index + 1) % 4])
			elif character == "s":
				write_next = pop(stackstack[-1])
				the_field.put_char(the_field.xy[1] + the_field.direction[1],
									the_field.xy[0] + the_field.direction[0], write_next)
				the_field.step()
			elif character == "w":
				a = pop(stackstack[-1])
				b = pop(stackstack[-1])
				if b > a:
					the_field.change_direction_tuple(dirs[(current_index + 1) % 4])
				elif a > b:
					the_field.change_direction_tuple(dirs[(current_index - 1) % 4])
			elif character == "n":
				stackstack[-1] = []
			elif character == "x":
				dy = pop(stackstack[-1])
				dx = pop(stackstack[-1])
				the_field.change_direction_tuple((dx, dy))
			elif character == "k":
				maxiters = pop(stackstack[-1])
				if not maxiters:
					maxiters = 1
					do_instruction("r")
				else:
					the_field.step()
					do_instruction(the_field.current_char())
			elif character == "{":
				# Pop n
				transfer_amount = pop(stackstack[-1])
				transfer = []
				# New TOSS
				stackstack.append([])
				# Pop n elements
				if transfer_amount >= 0:
					for n in range(transfer_amount):
						transfer.append(pop(stackstack[-2]))
				elif transfer_amount < 0:
					for n in range(-transfer_amount):
						transfer.append(0)
				# Push transfer elements
				for t in transfer[::-1]:
					stackstack[-1].append(t)
				# Get storage offset
				stor_off = the_field.storage_offset
				# Push storage offset to SOSS
				stackstack[-2].append(stor_off[0])
				stackstack[-2].append(stor_off[1])
				# Get new storage offset
				the_field.change_storage_offset(the_field.xy[0] + the_field.direction[0],
												the_field.xy[1] + the_field.direction[1])
			elif character == "}":
				# If stackstack underflow
				if len(stackstack) == 1:
					do_instruction("r")
				else:
					# Pop n
					transfer_amount = pop(stackstack[-1])
					# Change storage offset to the top vector in SOSS
					the_field.change_storage_offset(pop(stackstack[-2]), pop(stackstack[-2]))
					# Transfers elements from TOSS to SOSS
					transfer = []
					if transfer_amount >= 0:
						for n in range(transfer_amount):
							transfer.append(pop(stackstack[-1]))
					elif transfer_amount < 0:
						for n in range(-transfer_amount):
							pop(stackstack[-2])
					# Push transfer elements
					for t in transfer[::-1]:
						stackstack[-2].append(t)
					# Pop stackstack[-1]
					pop(stackstack)
			elif character == "u":
				if len(stackstack) == 1:
					do_instruction("r")
				else:
					count = pop(stackstack[-1])
					transfer = []
					# SOSS -> TOSS if count > 0 else TOSS -> SOSS
					from_index = int((-3-sgn(count))/2)
					to_index = int((-3+sgn(count))/2)
					for n in range(abs(count)):
						transfer.append(pop(stackstack[from_index]))
					for t in transfer:
						stackstack[to_index].append(t)

			elif character == "&":
				try:
					stackstack[-1].append(int(inputbox.ask(screen, "Put a number in the stack")))
				except Exception:
					return
			elif character == "~":
				if not instring:
					instring = list(inputbox.ask(screen, "Put a string to the stack"))
					instring.append(-1)
					instring = instring[::-1]
					stackstack[-1].append(ord(instring.pop()))
				else:
					if instring[len(instring)-1] == -1:
						stackstack[-1].append(int(instring.pop()))
					else:
						stackstack[-1].append(ord(instring.pop()))
		elif character == "\"":
			the_field.read_unichr(False)
			read_space = True
		elif character == ";":
			the_field.do_nothing(False)
		elif the_field.read or the_field.read_once:
			read_char = ord(character)
			if read_char == 32 and read_space:
				read_space = False
				stackstack[-1].append(read_char)
			elif read_char != 32:
				stackstack[-1].append(read_char)
		if maxiters == 1:
			the_field.step()
		if just_read:
			just_read = not just_read
		elif the_field.read_once:
			the_field.read_unichr_once(False)
	maxiters = 1


def run_code():
	global the_field
	global stackstack
	global outsurf
	global stackfont

	def initiate_new_run():
		render_code(the_field.code)
		screen.blit(background, (0, 0))
		screen.blit(stacksurf, (0, SCREENHEIGHT-200))
		toss_text = stackfont.render("TOSS", 1, STACKOUTPUTCOLOR)
		soss_text = stackfont.render("SOSS", 1, STACKOUTPUTCOLOR)
		stacksurf.blit(toss_text, (0, 0))
		stacksurf.blit(soss_text, (SCREENWIDTH/4, 0))
		screen.blit(outsurf, (int(float(SCREENWIDTH)/2.0), SCREENHEIGHT-200))
		screen.blit(cursor, (the_field.xy[0]*CHARWIDTH, the_field.xy[1]*CHARHEIGHT))
		pygame.display.flip()
	paused = False
	step1 = False
	reset = False
	pygame.display.set_caption("Befunge-93 Interpreter")
	background.fill(BGCOLOR)
	outsurf.fill((0, 0, 0, 100))
	stacksurf.fill((0, 0, 0, 100))
	cursor.fill((255, 255, 255, 130))
	# Event loop
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
		screen.blit(background, (0, 0))
		background.fill(BGCOLOR)
		screen.blit(stacksurf, (0, SCREENHEIGHT-200))
		screen.blit(outsurf, (int(float(SCREENWIDTH)/2.0), SCREENHEIGHT-200))
		stacksurf.fill((0, 0, 0, 100))
		toss_text = stackfont.render("TOSS", 1, STACKOUTPUTCOLOR)
		soss_text = stackfont.render("SOSS", 1, SOSSOUTPUTCOLOR)
		stacksurf.blit(toss_text, (0, 0))
		stacksurf.blit(soss_text, (SCREENWIDTH/4, 0))
		screen.blit(cursor, (the_field.xy[0]*CHARWIDTH, the_field.xy[1]*CHARHEIGHT))
		do_instruction(the_field.current_char())
		# Print stack (TOSS)
		for x, s in enumerate(stackstack[-1][::-1]):
			try:
				printstack = stackfont.render("{}. {} [{}] ({})".format(x+1,
												s, hex(s), chhr(s)), 1, STACKOUTPUTCOLOR)
			except Exception:
				printstack = stackfont.render("{}. {} ({})".format(x+1,
												s, chhr(s)), 1, STACKOUTPUTCOLOR)
			stacksurf.blit(printstack, (0, STACKCHARHEIGHT*x+20))
		# Print SOSS if it exists
		if len(stackstack) >= 2:
			for x, s in enumerate(stackstack[-2][::-1]):
				try:
					printstack = stackfont.render("{}. {} [{}] ({})".format(x+1,
													s, hex(s), chhr(s)), 1, SOSSOUTPUTCOLOR)
				except Exception:
					printstack = stackfont.render("{}. {} ({})".format(x+1,
													s, chhr(s)), 1, SOSSOUTPUTCOLOR)
				stacksurf.blit(printstack, (SCREENWIDTH/4, STACKCHARHEIGHT*x+20))
		try:
			pygame.time.wait(int(sys.argv[2]))
		except Exception:
			pygame.time.wait(50)
	with open(sys.argv[1], "r") as c:
		codelist = c.read().splitlines()
	the_field = Field(codelist)
	for x in enumerate(stackstack):
		stackstack[x] = []
	run_code()


if __name__ == '__main__':
	run_code()
	pygame.quit()
