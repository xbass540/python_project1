def get_average():
    with open('files/data.txt','r') as file:
        data = file.readlines()

    values = data[1:] #removes the first list item - temperatures
    values = [float(i) for i in values] # converts all items into floats
    return values


average = get_average()
print(average)
