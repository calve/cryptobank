import random

def randomword(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))
