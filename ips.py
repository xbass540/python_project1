ips = ['100.122.133.105', '100.122.133.111']

index = input("Input an index 0/1")

match index:
    case '0':
        print("You chose", ips[0])
    case '1':
        print("You chose", ips[1])
