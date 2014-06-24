class Field(object):
    def __init__(self, code):
        self.Y = len(code)
        self.X = max([len(code[l]) for l in range(self.Y)])
        self.code = []
        for c in code:
            if self.X > len(c):
                c += " " * (self.X - len(c))
            self.code.append(list(c))
        self.read = False
        self.read_once = False
        self._do_nothing = False
        self._storage_offset = (0, 0)

    def print_field(self, font):
        for c in self.code:
            print("".join(c))

    def read_unichr(self, bool_value):
        self.read = bool_value

    def read_unichr_once(self, bool_value):
        self.read_once = bool_value

    @property
    def do_nothing(self):
        return self._do_nothing

    @do_nothing.setter
    def do_nothing(self, value):
        self._do_nothing = value

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
    def __init__(self, init_pos, init_dir):
        super().__init__(codelist)
        self._xy = init_pos
        self._direction = init_dir

    def __repr__(self):
        return self._xy

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