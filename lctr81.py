while True:
    user_action = input("Type add, show, edit, complete or exit ")
    user_action = user_action.strip() #strips the white spaces from the string
    match user_action:
        case 'add':
            todo = input("enter a todo ")+"\n"

            with open('todos.txt', 'r') as file:
                todos = file.readlines()

            todos.append(todo)

            with open('todos.txt', 'w') as file:
                file.writelines(todos)

        case 'show':
            file=open("todos.txt", 'r')
            todos = file.readlines()

            for index, item in enumerate(todos):
                item=item.strip('\n')
                row=f"{index+1}-{item}"
                print(row)

        case 'exit':
            break

        case 'edit':

            number=int(input("Enter the number of the item to edit"))
            number = number-1

            with open('todos.txt', 'r') as file:
                todos = file.readlines()
                print("this is existing todos", todos)

            new_todo=input("Insert a new todo")
            todos[number]=new_todo + '\n'

            print('here is how it will be', todos)

            with open('todos.txt', 'w') as file:
                file.writelines(todos)

        case 'complete':

            number = int(input("Which item you want to remove"))

            with open('todos.txt', 'r') as file:
                todos = file.readlines()
            todo_to_remove = todos[number-1].strip("\n")# this removed the line brake at the end of the string
            todos.pop(number-1)

            with open('todos.txt', 'w') as file:
                todos = file.writelines(todos)

            message = f"Todo {todo_to_remove} was removed from the list"

            print(message)

print("bye")