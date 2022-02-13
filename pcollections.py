import re, traceback, keyword

def pnamedtuple(type_name, field_names, mutable = False,  defaults =  {}):
    def show_listing(s):
        for line_number, text_of_line in enumerate(s.split('\n'),1):         
            print(f' {line_number: >3} {text_of_line.rstrip()}')

    # put your code here
    # bind class_definition (used below) to the string constructed for the class
    class_definition = f'{type_name}("{field_names}", {mutable})'

    # Debugging aid: uncomment next call to show_listing to display source code
    # show_listing(class_definition)
    
    # Execute str in class_definition in name_space; then bind the attribute
    #   source_code to the class_definition str; finally, return the class
    #   object created; any syntax errors will print a listing of the
    #   of class_definition and trace the error (see the except clause).
    name_space = dict( __name__ = f'pnamedtuple_{type_name}' )                  
    try:
        exec(class_definition,name_space)
        name_space[type_name].source_code = class_definition
    except (TypeError,SyntaxError):                      
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]


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
        replacers = dict(kargs)
        
        if self._mutable:
            for key in replacers.keys():
                self.__dict__[key] = replacers[key]
        else:
            if 'x' not in replacers:
                return Point(kargs, x=self.get_x())
            elif 'y' not in replacers:
                return Point(kargs, y=self.get_y())
        
        
if __name__ == '__main__':
    # Test simple pnamedtuple below in script: Point=pnamedtuple('Point','x,y')
    point = Point(x=1, y=1)
    print(point)
    print(point._replace(x=2))
    print(point)
    #driver tests
    import driver  
    driver.default_file_name = 'bscp3W22.txt'
#     driver.default_show_exception_message = True
#     driver.default_show_traceback = True
    driver.driver()
