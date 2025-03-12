# Andrew Ngo
# azngo@uci.edu
# 63263981

from Profile import *
from pathlib import Path
from shlex import split as sh_split

menu = f"""{'-'*128}
C - Create a new DSU file
D - Delete an existing DSU file
R - Read contents of an existing DSU file
O - Load an existing DSU file
E - Add posts or edit contents of the current DSU file opened
P - Print contents of the current DSU file opened
S - Save a post to a DSP server from the current DSU file opened
Q - Quit the program
{'-'*128}"""
edit_options = f"""Edit options:
[-usr]      - Edit username
[-pwd]      - Edit password
[-bio]      - Edit bio
[-addpost]  - Write a new post to the file
[-delpost]  - Delete an existing post"""
print_options = f"""Print options:
[-usr]      - Print username
[-pwd]      - Print password
[-bio]      - Print bio
[-posts]    - Print ALL posts
[-post]     - Print a specific post
[-all]      - Print all info"""


# Prompts user for a command, returns the command as a string.
# If user enters "admin", returns False.
def get_command():
    global menu
    print(menu)
    command = input(">>> What would you like to do? ").strip()
    if command == 'admin':
        return True
    elif command not in ('C', 'O', 'R', 'P', 'E', 'D', 'Q', 'S'):
        raise ValueError("Sorry, that command wasn't recognized. Try again.")

    return command


# Prompts user for file path, name, username, password, and bio (optional).
# Returns the file's path as a string.
def file_creation():
    file_path = input(">>> Enter a directory to create your file in: ")
    if file_path[0] == "\"" and file_path[-1] == "\"":
        file_path = file_path[1:-1]

    file_path = Path(file_path)

    if not file_path.exists():
        raise NotADirectoryError("--- DIRECTORY NOT FOUND ---")
    elif not file_path.is_dir():
        raise NotADirectoryError("--- SPECIFIED PATH IS NOT A DIRECTORY ---")

    file_name = input(">>> Enter the new file's name: ")
    if (file_name[0] == "\"" and file_name[-1] == "\"" or
            file_name[0] == "\'" and file_name[-1] == "\'"):

        file_name = file_name[1:-1]

    username = input(">>> Enter a username: ").strip()
    while not username:
        username = input("> You must enter a username: ").strip()
    password = input(">>> Enter a password: ").strip()
    while not password:
        password = input("> You must enter a password: ").strip()
    bio = input(">>> Enter a bio: ").strip()
    while not bio:
        bio = input(">>> You must enter a bio: ").strip()
    dsuserver = input(">>> Specify a DSU server to publish journals in, "
                      "or press ENTER for default ('127.0.0.1'): ").strip()
    if not dsuserver:
        dsuserver = '127.0.0.1'

    return (file_path, file_name, username, password, bio, dsuserver)


# Prompts user for a DSU file path. Returns a Path object.
def file_deletion():
    file_path = input(">>> Enter the path of the file you wish to delete: ")
    if file_path[0] == "\"" and file_path[-1] == "\"":
        file_path = file_path[1:-1]
    file_path = Path(file_path)

    if not file_path.exists() and file_path.suffix == '.dsu':
        raise FileNotFoundError("--- FILE DOES NOT EXIST OR IS NOT TYPE"
                                "(DSU) ---")

    return file_path


def file_reading():
    file_path = input(">>> Enter the path of the file you wish to read: ")
    if file_path[0] == "\"" and file_path[-1] == "\"":
        file_path = file_path[1:-1]
    file_path = Path(file_path)

    if not file_path.exists() and file_path.suffix == '.dsu':
        raise FileNotFoundError("--- FILE DOES NOT EXIST OR IS NOT TYPE"
                                "(DSU) ---")

    return file_path


def file_opening():
    file_path = input(">>> Enter the path of the file you wish to open for"
                      "editing/printing: ")
    if file_path[0] == "\"" and file_path[-1] == "\"":
        file_path = file_path[1:-1]
    file_path = Path(file_path)

    if not file_path.exists() and file_path.suffix == '.dsu':
        raise FileNotFoundError("--- FILE DOES NOT EXIST OR IS NOT TYPE"
                                "(DSU) ---")

    return file_path


def file_editing(current_file: str):
    if not current_file:
        raise FileNotFoundError("Sorry, you haven't opened a file yet!\n"
                                "First use (O) to open an existing file, "
                                "or (C) to create a new file.")

    print(edit_options)
    option = input(">>> Choose an editing option: ")
    while (option not in ('-usr', '-pwd', '-bio', '-addpost', '-delpost')):
        if input(">>> Sorry, you entered an invalid option. "
                 "Try again? (y/n): ").strip().lower() == 'y':
            print(edit_options)
            option = input(">>> Choose an editing option: ")
        else:
            return False
    if option == '-usr':
        info = input(">>> Enter a new username: ").strip()
    elif option == '-pwd':
        info = input(">>> Enter a new password: ").strip()
    elif option == '-bio':
        info = input(">>> Enter a new bio: ").strip()
        update = input(">>> Would you like to update your bio to the server? "
                       "(y/n): ").strip().lower()
        if update == 'y':
            return [option, info, True]
        else:
            return [option, info, False]
    elif option == '-addpost':
        info = input(">>> Enter a post: ").strip()
        update = input(">>> Would you like to save your post to the server? "
                       "(y/n): ").strip().lower()
        if update == 'y':
            return [option, info, True]
        else:
            return [option, info, False]
    elif option == '-delpost':
        p = Profile()
        p.load_profile(current_file)

        for i in range(len(p.get_posts())):
            print(f"{i} - {p.get_posts()[i].get_entry()}")
        info = input(">>> Enter the post index you wish to delete: ").strip()

        if not info.isnumeric or not int(info) in range(len(p.get_posts())):
            raise TypeError(f"Sorry, \"{info}\" is not a valid post index!")

        info = int(info)

    return [option, info]


def file_printing(current_file: str):
    if not current_file:
        raise FileNotFoundError("Sorry, you haven't opened a file yet!\n"
                                "Use the (O) command to open an existing "
                                "file, or (C) to create a new file.")

    print(print_options)
    option = input(">>> Choose a printing option: ")
    while (option not in ('-usr', '-pwd', '-bio', '-posts', '-post', '-all')):
        if input(">>> Sorry, you entered an invalid option. "
                 "Try again? (y/n): ").strip().lower() == 'y':
            print(print_options)
            option = input(">>> Choose a printing option: ")
        else:
            return False
    p = Profile()
    p.load_profile(current_file)

    if option == '-post':
        index = input(f">>> Enter a post's ID number from "
                      f"0 - {len(p.get_posts())-1}: ")
        if not index.isnumeric():
            raise TypeError(f"Sorry, \"{index}\" is not a valid post ID!")
        return [option, int(index)]

    else:
        return [option]


def publishing(current_file: str):
    if not current_file:
        raise FileNotFoundError("Sorry, you haven't opened a file yet!\n"
                                "Use the (O) command to open an existing "
                                "file, or (C) to create a new file.")

    print("1 - Save a post\n"
          "2 - Save a bio\n"
          "3 - Save both a post and bio")
    option = input(">>> Enter an option: ")
    if not option.isnumeric() or int(option) not in (1, 2, 3):
        raise ValueError(f"Sorry, \"{option}\" is not a valid option!")
    option = int(option)

    p = Profile()
    p.load_profile(current_file)
    all_posts = p.get_posts()

    post = ""
    bio = ""
    if option == 1 or option == 3:
        if len(all_posts) == 0:
            raise ValueError("You have no posts currently. "
                             "Please create a post using the editing command "
                             "(E) before trying to publish.")

        for i in range(len(all_posts)):
            print(f"{i} - {all_posts[i].get_entry()}")
        index = input(">>> Enter the post ID you'd like to publish: ")
        if not index.isnumeric() or not int(index) in range(len(all_posts)):
            raise TypeError(f"Sorry, \"{index}\" isn't a valid post ID!")
        post = all_posts[int(index)].get_entry()

    if option == 2 or option == 3:
        bio = input("Enter a new bio: ").strip()

    return (post, bio)
