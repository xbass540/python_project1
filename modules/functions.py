FILEPATH = "todos.txt"

def get_todos(filepath=FILEPATH):
    """
    Read a taxt file and return
    the list of todos
    :param filepath: default parameter
    :return: the list of todos
    """
    with open(filepath, 'r') as file_local:
        todos_local = file_local.readlines()
    return todos_local


def write_todos( todos_arg, filepath_arg=FILEPATH):
    """

    :param todos_arg: list input
    :param filepath_arg: default file to write
    :return: nothing
    """
    with open(filepath_arg, 'w') as file:
        file.writelines(todos)

print(__name__)

if __name__=="__main__":
    print("Hello")