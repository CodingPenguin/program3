# Submitter: bryanttp(Phan, Bryant)
# Partner  : dannyhn5(Nguyen, Danny)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming
  
import re, traceback, keyword

def pnamedtuple(type_name, field_names, mutable = False,  defaults =  {}):
    def show_listing(s):
        for line_number, text_of_line in enumerate(s.split('\n'),1):         
            print(f' {line_number: >3} {text_of_line.rstrip()}')

    # put your code here
    # bind class_definition (used below) to the string constructed for the class
    
    pattern = r'[a-zA-Z][\w]*'
    
    # type_name legality
    if type(type_name) != str or type_name in keyword.kwlist or not bool(re.match(pattern, type_name)):
        raise SyntaxError(f'{type_name} is not a legal string or is a keyword')
    
    # field_names legality
    if type(field_names) == list: names = field_names
    elif type(field_names) == str: names = re.split("[, ]+", field_names)
    else: raise SyntaxError(f'{field_names} must be of type list or str')
    for name in names:
        if name in keyword.kwlist or not bool(re.match(pattern, name)):
            raise SyntaxError(f'{name} is not a legal string or is a keyword')
        
    # defaults legality
    for key in defaults:
        if key not in names:
            raise SyntaxError(f'{key} not a valid argument name')
    
    class_template = '''\
class {class_name}:
    _fields = {fields}
    _mutable = {mutable}
    
    {init_block}
    
    {repr_block}
    
    {get_block}
    
    {getitem_block}
    
    {eq_block}
    
    {_asdict_block}
    
    {_make_block}
    
    {_replace_block}
'''

    def gen_init() -> str:
        my_string = 'def __init__(self, {params}):\n'.format(params = ', '.join([name if name not in defaults else f'{name}={defaults[name]}' for name in names]))
        for name in names:
            my_string += '''        self.{name} = {name}\n'''.format(name=name)
        return my_string
        
    def gen_repr():   
        field_args = []
        for field_name in names:
            field_args.append(f'{field_name}=self.{field_name}')
        
        return '''
    def __repr__(self):
        return '{class_name}({field_args})' '''.format(class_name=type_name, field_args=','.join(field_args))
    
    def gen_get():
        get_funcs = ''
        for field_name in names:
            get_funcs += '''
    def get_{name}(self):
        return self.{name}
        '''.format(name=field_name)
        return get_funcs
    
    def gen_getitem():
        return '''
    def __getitem__(self, idx):
        if type(idx) == int and idx in range(len(self._fields)):
            return eval(f'self.get_{self._fields[idx]}')
        elif type(idx) == str and idx in self._fields:
            return eval(f'self.get_{idx}')
        else:
            raise IndexError'''
    
    def gen_eq():
        return '''
    def __eq__(self, comparison):
        if type(comparison) == type(self):
            for idx in range(len(self._fields)):
                if self.__getitem__(idx) != comparison.__getitem__(idx):
                    return False
            return True
        else:
            return False'''
    
    def gen_asdict():
        add_keys = ''
        for field_name in names:
            add_keys += '''
        attr_dict[{field_name}] = self.get_{field_name}()'''.format(field_name = field_name)
        return '''
    def _asdict():
        attr_dict = {{}}
        {add_keys}'''.format(add_keys=add_keys)
        
    def gen_make():
        return '''
    @staticmethod
    def _make(iterable):
        return {type_name}(*iterable)'''.format(type_name = type_name)
    
    def gen_replace():
        return '''
    def _replace(**kargs):
        for karg in kargs:
            if karg not in {names}:
                raise TypeError
        if self._mutable:
            for karg in kargs:
                exec(f'self.{{karg}} = {{kargs[karg]}}')
            return None
        else:
            return {type_name}(**kargs)'''.format(names = names, type_name = type_name)
                
    class_definition = class_template.format(class_name = type_name, fields = names, mutable = mutable, init_block = gen_init(), repr_block = gen_repr(), get_block = gen_get(), getitem_block = gen_getitem(), eq_block = gen_eq(), _asdict_block = gen_asdict(), _make_block = gen_make(), _replace_block = gen_replace())

    # Debugging aid: uncomment next call to show_listing to display source code
    #show_listing(class_definition)
    
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


    
if __name__ == '__main__':
    # Test simple pnamedtuple below in script: Point=pnamedtuple('Point','x,y')

    #driver tests
    import driver  
    driver.default_file_name = 'bscp3W22.txt'
#     driver.default_show_exception_message = True
#     driver.default_show_traceback = True
    driver.driver()
