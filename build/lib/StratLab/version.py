def get_version():
    with open('StratLab/__vrsn__.txt', 'r') as file:
        version = file.read()
        print(version)
    return version

get_version()