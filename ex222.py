user_prompt = input("give me a new member") # asks the user to enter a name

file = open('files/members.txt', 'r') # opens the file for reading
intermittent_variable = file.readlines() # assigns the content of the file to the inter list

intermittent_variable.append(user_prompt+"\n") # final text is a list that contains the initial file contents + the new user prompt

file.close()


file = open('files/members.txt', 'w') # opens the file for reading
file.writelines(intermittent_variable)
