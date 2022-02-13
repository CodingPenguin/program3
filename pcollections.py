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
    class_template = '''\
    class {class_name}:
        _fields = [{fields}]
        _mutable = {mutable}
        
        {init_block}
        
        {repr_block}
        
        {get_block}
        
        {getitem_block}
        
        {eq_block}
        
        {_asdict_block}
        
        {_make_block}
        
        {_replace_block}
        
        #{setattr_block} 
    '''

    def gen_init():
        self_assign = ''
        default_params = ''
        for field_name in field_names:
            self_assign += f'self.{field_name} = {field_name}\n'
            
        for idx, key in enumerate(defaults.keys()):
            default_params += f'{key}={defaults[key]}, ' if idx < len(list(defaults.keys())) - 1 else f'{key}={defaults[key]}'
            
        return \
            '''
                def __init__(self, {default_params}):
                    {assignments}
            '''.format(default_params=default_params, assignments=self_assign)
        
    def gen_repr():
        if type(field_names) == str:
            field_names = field_names.replace(',', ' ')
            field_names = field_names.split()
        
        field_args = ''
        for idx, field_name in enumerate(field_names):
            if idx == len(field_names) - 1:
                field_args += f'self.{field_name}={field_name}'
            field_args += f'self.{field_name}={field_name},'
        
        return \
        '''
            def __repr__(self):
                return {class_name}({field_args})
        '''.format(class_name=type_name, field_args=field_args)
    
    def gen_get():
        get_funcs = ''
        for field_name in field_names:
            get_funcs += \
                '''
                    def get_{name}(self):
                        return self.{name}
                '''.format(name=field_name)
        
        return get_funcs
    
    def gen_getitem(i: int):
        field = field_names[i]
        return eval(f'self.get_{field}()')
    
    def gen_eq():
        eq_ifs = ''
        for idx in range(len(field_names)):
            eq_ifs += \
                '''
                    if self.__getitem__({index}) != comparison.__getitem__({index}):
                        return False
                '''
        return \
            '''
                def __eq__(self, comparison):
                    if type(comparison) == type(self):
                        {eq_ifs}
                        return True
            '''.format(eq_ifs=eq_ifs)
    
    def gen_asdict():
        add_keys = ''
        for field_name in field_names):
            add_keys += \
            '''
                attr_dict[{field_name}] = self.get_{field_name}()
            '''
        return \
            '''
                attr_dict = {}
                {add_keys}
            '''.format(add_keys=add_keys)
            
    def gen_make():
        pass
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


    
if __name__ == '__main__':
    # Test simple pnamedtuple below in script: Point=pnamedtuple('Point','x,y')
    #driver tests
    import driver  
    driver.default_file_name = 'bscp3W22.txt'
#     driver.default_show_exception_message = True
#     driver.default_show_traceback = True
    driver.driver()
