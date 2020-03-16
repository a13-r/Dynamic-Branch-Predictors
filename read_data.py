def read_data():
    addresses = []
    decisions = []
    test_file = open("test.trace", "r")
    if test_file.mode == 'r':
        contents = test_file.read().split("\n")
        for line in contents:
            address = line[0: len(line) - 2]
            decision = line[len(line) - 1: len(line)]
            addresses.append(int(address))
            if decision == 'T':
                decisions.append(1)
            else:
                decisions.append(0)
    return addresses, decisions
