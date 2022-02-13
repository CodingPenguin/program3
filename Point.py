class Point:
    _fields = ['x', 'y']
    
    def __init__(self, x, y, mutable=False):
        self.x = x
        self.y = y
        self._mutable = mutable
    
    def __repr__(self):
        return f'Point(x={self.x}, y={self.y})'
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def __getitem__(self, idx):
        if idx == 0:
            return self.get_x()
        elif idx == 1:
            return self.get_y()
        else:
            raise IndexError('nope')
    
    def __eq__(self, comparison):
        if type(comparison) == type(self):
            if self.get_x() == comparison.get_x() and self.get_y() == comparison.get_y():
                return True
        return False
        
    def _asdict(self):
        return {'x': self.get_x(), 'y': self.get_y()}
    
    def _make(self, arg):
        x, y = arg
        return Point(x, y)
    
    def _replace(self, **kargs):
        
        if self._mutable:
            replacers = dict(kargs)
            for key in replacers.keys():
                self.__dict__[key] = replacers[key]
        else:
            if 'x' not in kargs:
                return Point(kargs, x=self.get_x())
            elif 'y' not in kargs:
                return Point(kargs, y=self.get_y())