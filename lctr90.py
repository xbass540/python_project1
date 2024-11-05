while True:
    user_action = input("Type add, show, edit, complete or exit ")
    user_action = user_action.strip() #strips the white spaces from the string

    if user_action.startswith('add'):
        todo = user_action[4:]

        with open('todos.txt', 'r') as file:
            todos = file.readlines()

        todos.append(todo + "\n")

        with open('todos.txt', 'w') as file:
            file.writelines(todos)

    elif user_action.startswith('show'):
        file=open("todos.txt", 'r')
        todos = file.readlines()

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

            with open('todos.txt', 'r') as file:
                todos = file.readlines()
                print("this is existing todos", todos)

            new_todo=input("Insert a new todo")
            todos[number]=new_todo + '\n'

            print('here is how it will be', todos)

            with open('todos.txt', 'w') as file:
                file.writelines(todos)

        except ValueError:
            print("Enter a valid command")
            continue #goes back to the beginning of the loop

    elif user_action.startswith('complete'):
        try:
            number = int(user_action[9:])

            with open('todos.txt', 'r') as file:
                todos = file.readlines()
            todo_to_remove = todos[number-1].strip("\n")# this removed the line brake at the end of the string
            todos.pop(number-1)

            with open('todos.txt', 'w') as file:
                todos = file.writelines(todos)

            message = f"Todo {todo_to_remove} was removed from the list"
            print(message)
        except IndexError:
            print("There is no such item index")
            continue


    else:
        print("Not valid command")

print("bye")