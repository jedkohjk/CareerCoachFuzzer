from random import random

# Shared generator functions

# Takes a random slice of the string
def random_slice(string: str) -> str:
    op = ''
    while not op:
        op = string[int(len(string)*random()):int(len(string)*random())+1].strip()
    return op

# Randomise case of letters in string
def random_case(string: str):
    return ''.join(i.upper() if int(random()*2) else i.lower() for i in string)
