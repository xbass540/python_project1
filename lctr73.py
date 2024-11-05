while True:
    user_action = input("Type add, show, edit or exit ")
    user_action = user_action.strip() #strips the white spaces from the string
    match user_action:
        case 'add':
            todo = input("enter a todo ")+"\n"

            file=open("../todos.txt", 'r')
            todos = file.readlines()
            file.close()

            todos.append(todo)

            file = open('../todos.txt', 'w')
            file.writelines(todos)
            file.close()
        case 'show':
            file=open("todos.txt", 'r')
            todos = file.readlines()
            file.close()



            for index, item in enumerate(todos):
                item=item.strip('\n')
                row=f"{index+1}-{item}"
                print(row)

        case 'exit':
            break
        case 'edit':
            number=int(input("Enter the number of the item to edit"))
            number = number-1
            new_todo=input("Insert a new todo")
            todos[number]=new_todo
            print(existing_todo)
        case 'complete':
            number = int(input("Which item you want to remove"))
            todos.pop(number)
print("bye")