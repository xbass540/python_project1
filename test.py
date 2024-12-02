import sinmodule

'''user_update = []
user_input = []
numbers = []
while user_input!='0':
    user_input = input("give me 1 number to store in the file: ")
    user_input.strip()

    with open('numbers.txt', 'w') as file:
        user_update.append(user_input+'\n')
        file.writelines(user_update)

with open('numbers.txt', 'r') as file:
    file_output = file.readlines()
    file_output.pop()
    file_output.sort()
    for index,item in enumerate(file_output):
        print(f"{index}. {file_output[index]}")
'''

#print(sinmodule.sin_function(sin_input))

file_record = []
sin_input = []

while sin_input != 'exit':
    try:
        sin_input = input('give me a sin to calculate')+"\n"
        with open('numbers2.txt', 'w') as file:
            sin_calculation = sinmodule.sin_function(sin_input)# calculates sin using the module function
            file_record.append(sin_calculation)
            file_record.append(+'\n')
            file.writelines(str(file_record))
    except ValueError:
        print('not valid entry')
