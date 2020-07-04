import random
import string


def generate_string():
    return ''.join(random.choice(string.ascii_letters) for _ in range(8))
