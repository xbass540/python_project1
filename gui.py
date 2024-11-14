from modules import functions
import FreeSimpleGUI as sg

label = sg.Text("Type in a to do")
input_box = sg.InputText(tooltip="Enter a todo")
add_button = sg.Button("Add")

window = sg.Window('My To-Do app', layout=[[label],[input_box,add_button]])


window.read()#displays window on the screen
print("Hello")
window.close()