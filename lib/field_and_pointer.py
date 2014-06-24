import six
import sys


class Field(object):
    '''
    This is the class handling the Funge-space, being the code field
    in Befunge.
    '''
    def __init__(self, code):
        self.Y = len(code)
        self.X = max([len(code[l]) for l in range(self.Y)])
        self.code = []
        for c in code:
            if self.X > len(c):
                c += " " * (self.X - len(c))
            self.code.append(list(c))
        self._storage_offset = (0, 0)

    def print_field(self, font):
        for c in self.code:
            print("".join(c))

    def get_char(self, xget, yget):
        return self.code[yget % self.Y][xget % self.X]

    def put_char(self, yput, xput, v):
        ynew = yput + self.storage_offset[1]
        xnew = xput + self.storage_offset[0]
        self.code[ynew % self.Y][xnew % self.X] = chhr(v)

    @property
    def storage_offset(self):
        return self._storage_offset

    @storage_offset.setter
    def storage_offset(self, value):
        self._storage_offset = value


class Pointer(Field):
    '''
    This is the class handling the instruction pointer, which inherits
    from the code field.
    '''
    def __init__(self, init_pos, init_dir):
        super().__init__(load_code())
        self._xy = init_pos
        self._direction = init_dir
        self._maxiters_k = 1
        self._read_space = True
        self._read = False
        self._read_once = False
        self._do_nothing = False

    def __repr__(self):
        return self.__get__()

    @property
    def do_nothing(self):
        return self._do_nothing

    @do_nothing.setter
    def do_nothing(self, value):
        self._do_nothing = value

    @property
    def read(self):
        return self._read

    @read.setter
    def read(self, value):
        self._read = value

    @property
    def read_once(self):
        return self._read_once

    @read_once.setter
    def read_once(self, value):
        self._read_once = value

    @property
    def read_space(self):
        return self._read_space

    @read_space.setter
    def read_space(self, value):
        self._read_space = value

    @property
    def maxiters_k(self):
        return self._maxiters_k

    @maxiters_k.setter
    def maxiters_k(self, value):
        self._maxiters_k = value

    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, value):
        self._xy = value

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, newdir):
        dirs = {"up": (0, -1), "down": (0, 1),
                "left": (-1, 0), "right": (1, 0)}
        if type(newdir) is str:
            self._direction = dirs[newdir]
        elif type(newdir) is tuple:
            self._direction = newdir

    def step(self):
        self._xy = ((self._xy[0] + self._direction[0]) % self.X,
                   (self._xy[1] + self._direction[1]) % self.Y)

    def stop(self):
        self.direction = (0, 0)

    def current_char(self):
        return self.code[self.xy[1] % self.Y][self.xy[0] % self.X]


def chhr(tal):
    '''
    Modified and tried to generalize the chr() function to
    match the behavior of the stack in Befunge.
    '''
    if tal <= 0:
        return " "
    else:
        return six.unichr(tal)


def load_code():
    '''
    Loads the Befunge code from an external file.
    '''
    try:
        with open(sys.argv[1], "r") as c:
            codelist = c.read().splitlines()
        if codelist:
            return codelist
        else:
            return [" "]
    except IndexError:
        raise IOError("Run as 'python bf98.py <befunge file> [speed]'")
