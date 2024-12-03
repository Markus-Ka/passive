from .options import options_map
import sys
import ipaddress

def input_check(args):
    key = args[0]
    values = args[1:]
    
    key_check(key)
    length_check(values, key)
    
    match key:
        case "--help":
            return
        case "-fn":
            valid_full_name_check(values)
            return
        case "-ip":
            valid_ip_check(values)
            return
        case "-u": # I guess any username is valid?
            valid_username_check(values)
            return
        case _:
            print("Default case in input_check, shouldnt end up here, contact admin")
            sys.exit(0)


def valid_username_check(values): # @username ?? what is a valid username
    pass

def valid_ip_check(values):
    try:
        ipaddress.ip_address(values[0])
        return
    except ValueError:
            print(f'Not a valid ip address "{values[0]}"')
            sys.exit(0)



def valid_full_name_check(values):
    names = values[0].split()
    for value in names:
        if value.isalpha():
            continue
        else:
            print(f'Not a valid name "{value}"')
            print("Please enter alphabetical caracters only")
            sys.exit(0)
    return



def key_check(key):
    if key in options_map:
        return            
    else:
        print(f'Incorrect flag: "{key}"')
        print('Run "--help" for instructions')
        sys.exit(0)

    
def length_check(values, key):
    if options_map[key]['arg_length'] == len(values) or key == "--help":
        return
    else:
        print(f"Incorrect number of arguments, have {len(values)} needs {options_map[key]['arg_length']}")
        print(f"Args: {values}")
        if key == "-fn":
            print('Example: passive -fn "firstname lastname"')
        if key == "-u":
            print('Example: passive -u "@username"')
        if key == "-ip":
            print("Example: passive -ip 127.0.0.1")
        sys.exit(0)