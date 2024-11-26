from modules import functions
import FreeSimpleGUI as sg

label = sg.Text("Type in a to do")
input_box = sg.InputText(tooltip="Enter a todo", key = "todo")
add_button = sg.Button("Add")
list_box = sg.Listbox(values = functions.get_todos(), key='todos',
                      enable_events = True, size=[45,10])
edit_button = sg.Button("Edit")

window = sg.Window('My To-Do app',
                   layout=[[label],[input_box,add_button], [list_box, edit_button]],
                   font=('Helvetica',20))

while True:
    event, values = window.read()#displays window on the screen
    print(1, event)# this is the even returned when i click a list item
    print(2, values)# the value i write inside the input field and the clicked item value
    print(3, values['todos'])# the value of

    match event:
        case "Add":
            todos = functions.get_todos()
            new_todo = values['todo'] + "\n"#this is the value of the key named todo.
                                    # it is a dictionary
            todos.append(new_todo)
            functions.write_todos(todos)
            window['todos'].update(values=todos)#update list with the new item
        case sg.WIN_CLOSED:#close window button
            break
        case "Edit":
            todo_to_edit = values['todos'][0]
            new_todo = values['todo']

            todos = functions.get_todos()
            index = todos.index(todo_to_edit)
            todos[index] = new_todo
            functions.write_todos(todos)
            window['todos'].update(values = todos)
        case 'todos':
            window['todo'].update(value=values['todos'][0])
window.close()