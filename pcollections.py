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
