from string import ascii_lowercase, digits
import random


alphanum = ascii_lowercase + digits
def randstr(count:int=48):
    return ''.join([alphanum[random.randint(0, 35)] for _ in range(count)])

# print(randstr())
