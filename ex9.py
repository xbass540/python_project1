filenames = ['document', 'report', 'presentation']

for index,item in enumerate(filenames):
    item = item.capitalize()
    output=f"{index}-{item}.txt"
    print(output)