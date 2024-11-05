user_prompt = "Enter a todo: "

todos = []

while True:
    user_action = input("Type add, show or exit ")
    user_action=user_action.strip()

    match user_action:
        case 'add':
            todo = input("enter a todo ")
            todos.append(todo)
        case 'show':
            for item in todos:
                print(item)
        case 'exit':
            break
        case _:
            print("Wrong Command")

print("Bye")