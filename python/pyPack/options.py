from .full_name_search import launch_full_name_search
from .ip_search import launch_ip_search
from .username_search import launch_username_search


def full_name_callback(options_map, args):
    launch_full_name_search(args)

def ip_callback(options_map, args):
    launch_ip_search(args[1])

def username_callback(options_map, args):
    launch_username_search(args[1])

def help_callback(options_map, args):
    print("Welcome to passive v1.0.0")
    print("OPTIONS:")
    for key, value in options_map.items():
        if key == "--help":
            continue
        print(f"{key:<10} {value['description']}")
        
    

options_map = {
        "-fn": {"description": "Search with full-name", "arg_length": 1, "callback": full_name_callback},
        "-ip": {"description": "Search with ip address", "arg_length": 1, "callback": ip_callback},
        "-u":  {"description": "Search with username", "arg_length": 1, "callback": username_callback},
        "--help": {"description": "", "arg_length": 0, "callback": help_callback}
    }
