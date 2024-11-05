date = input("what is the date?")
mood = input("what is your mood")
journal = input("let your thoughts flow:\n")

with open(f"journal/{date}.txt","w") as file:
    file.write(mood + 2*"\n")
    file.write(journal)