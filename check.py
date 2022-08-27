def compare(file_in, file_out, buffor):
    x = file_out.readlines()
    y = buffor.readlines()

    for line in range(len(x)):
        x[line] = x[line].replace("\n", "")
    for line in range(len(y)):
        y[line] = y[line].replace("\n", "")

    return x == y