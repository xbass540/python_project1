#from functions import get_todos, write_todos

from modules import functions

while True:
    user_action = input("Type add, show, edit, complete or exit ")
    user_action = user_action.strip() #strips the white spaces from the string

    if user_action.startswith('add'):
        todo = user_action[4:]

        todos = functions.get_todos()

        todos.append(todo + "\n")

        functions.write_todos(todos, "todos.txt")

    elif user_action.startswith('show'):
        todos = functions.get_todos()

        for index, item in enumerate(todos):
            item=item.strip('\n')
            row=f"{index+1}-{item}"
            print(row)

    elif user_action.startswith('exit'):
        break

    elif user_action.startswith('edit'):
        try:
            number = int(user_action[5:])
            number = number-1

            todos = functions.get_todos()
            print("this is existing todos", todos)

            new_todo=input("Insert a new todo")
            todos[number]=new_todo + '\n'

            print('here is how it will be', todos)

            functions.write_todos(todos, "todos.txt")

        except ValueError:
            print("Enter a valid command")
            continue #goes back to the beginning of the loop

    elif user_action.startswith('complete'):
        try:
            number = int(user_action[9:])

            todos = functions.get_todos()
            todo_to_remove = todos[number-1].strip("\n")# this removed the line brake at the end of the string
            todos.pop(number-1)

            functions.write_todos(todos, "todos.txt")

            message = f"Todo {todo_to_remove} was removed from the list"
            print(message)
        except IndexError:
            print("There is no such item index")
            continue


    else:
        print("Not valid command")

print("bye")