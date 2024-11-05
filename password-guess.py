user_prompt = "what is the password? "
question_var = input(user_prompt)

question_prompt = "Guess the password"
answer=input(question_prompt)

while answer!=question_var:
    question_prompt = "Guess the password"
    answer = input(question_prompt)

print("you found it!")

