# Befunge-98 Interpreter

This is a Befunge-98 interpreter written in python 3.4 with the use of pygame. The code has not properly been tested on python 2.X.

This is basically an extended version of my [Befunge-93 interpreter](https://github.com/johanasplund/befunge-93).

The full technical specification of the Funge-98 languages can be found [here](https://github.com/catseye/Funge-98/blob/master/doc/funge98.markdown).

Johan Asplund

## How to use
```
$ python bf98.py -h
usage: bf98.py [-h] [-s SPEED] [-o] [-y] befunge_file

A Befunge-98 interpreter written in pygame.

positional arguments:
  befunge_file   the full path to a befunge file to be interpreted

optional arguments:
  -h, --help     show this help message and exit
  -s SPEED       specify the time between each tick (default: 50 ms)
  -o             only show the output of the program in the shell
  -y, --sysinfo  show the environment variables used in the y instruction
```

### Controls
- `space` to pause the code
- `r` to reset the code
- `right arrow` to step once
- `esc` to quit

## TODO
- ~~Make the code more structured and/or clean up some~~
- ~~Add output only mode~~
- Add the `y` instruction
- Add the `t` instruction (aka Concurrent Befunge-98)
- Add fingerprints


### Other notes
The font *Inconsolata*, which is used in the interpreter, is owned by [Raph Levien](http://levien.com/type/myfonts/inconsolata.html).

# Quick reference for Befunge-98

*TOSS = Top of stack stack*

*SOSS = Second on stack stack*

*IP = Instruction pointer*

Character |Description 
 -------- | ---------- 
`0-9` | Push this number to the stack.
`a-f` | Push 10, ... ,15 to the stack.
`+` | Pop `a` and `b`, then push `a+b`.
`-` | Pop `a` and `b`, then push `a-b`.
`*` | Pop `a` and `b`, then push `a*b`.
`/` | Pop `a` and `b`, then push `floor(b/a)`, provided that `a` is not zero.
`%` | Pop `a` and `b`, then push `a (mod b)`.
`!` | Pop `a`. If `a = 0`, push 1, otherwise push 0.
<code>`</code> | Pop `a` and `b`, then push 1 if `b > a`, otherwise 0.
`w` | Pop `a` and `b`. Do instruction `]` if `a > b` otherwise if `b > a` do instruction `[`. If `a = b` do nothing.
`k` | Pop `n`. Iterate next instruction `n` times.
`>` | Move right.
`<` | Move left.
`^` | Move up.
`v` | Move down.
`?` | Move in a random direction.
`[` | Turn the IP CW 90 degrees.
`]` | Turn the IP CCW 90 degrees.
`r` | Turn the IP 180 degrees.
`x` | Pop `dx` and `dy`. Set the new direction vector to `(dx, dy)`.
`_` | Pop `a`. If `a = 0`, move right, otherwise move left.
<code>&#124;</code> | Pop `a`. If `a = 0` , move down, otherwise move up.
`"` | Start string mode. Push each characters ASCII value all the way up to the next ".
`'` | Start string mode for the next character only.
`(` | Load fingerprint (not implemented yet in this interpreter).
`)` | Unload fingerprint (not implemented yet in this interpreter).
`A-Z` | Defined by fingerprints.
`:` | Duplicate value on top of the stack.
`\` | Swap the two values on top of the stack.
`$` | Remove the value on top of the stack.
`n` | Empty stack.
`.` | Pop `a`. Output the integer value of `a`.
`,` | Pop `a`. Output `chr(a)`.
`#` | Skip next cell.
`;` | Skip every cell up until next `;`.
`j` | Pop `n`. Skip the next `n` cells.
`p` | Pop `y`, `y` and `v`. Change the character in position `(x,y)` *relative to the storage offset* to `chr(v)`.
`g` | Pop `y` and `x` , the push the ASCII value of the character in position `(x,y)` *relative to the storage offset*.
`s` | Pop `v` and push the ASCII value of the character to the next cell.
`&` | Prompt user for a number and push it.
`~` | Prompt user for a character and push its ASCII value.
`{` | Pop `n`. Push a new stack in the stack stack. Pop `n` elements from the SOSS and place them in the new TOSS (while preserving the ordering). Also pop the storage offset into SOSS.
`}` | Pop `n`. Pop `n` elements from the TOSS and place them in the SOSS (while preserving the ordering). Pop a stack from the stack stack.
`u` | Pop `n`. If `n > 0`, pop `n` elements from the SOSS and push each element to the TOSS (thus reversing their order). If `n < 0`, transfer `n` elements in the other direction.
`y` | Get sysinfo (not implemented yet in this interpreter).
`t` | Split cursor to allow multiple cursors (not implemented yet in this interpreter).
`@` | Stop IP.
