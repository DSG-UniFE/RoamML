with open("receiver_report","rt") as file:
    total = 0
    while True:
        line = file.readline()
        if not line:
            break
        filehash, filedim = line.split(",")
        dim = int(filedim)
        total += dim

    print(total)