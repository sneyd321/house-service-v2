
import string
import random
import hashlib
def generate_hash():
    return ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=6))

seen = set()

for i in range(0, 10000000):
    line = generate_hash()
    while line in seen:
        line = generate_hash()
    seen.add(line)

print(len(seen))