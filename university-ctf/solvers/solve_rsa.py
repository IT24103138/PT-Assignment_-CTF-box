
from pathlib import Path
import ast
import math

challenge_file = Path("../crypto02/rsa_challenge.txt")
data = {}

for line in challenge_file.read_text(encoding="utf-8").splitlines():
    key, value = line.split("=", 1)
    data[key.strip()] = ast.literal_eval(value.strip())

n = data["n"]
e = data["e"]
ciphertext = data["c"]

# Factor the deliberately small RSA modulus
p = None
q = None

for candidate in range(2, math.isqrt(n) + 1):
    if n % candidate == 0:
        p = candidate
        q = n // candidate
        break

if p is None:
    raise ValueError("Could not factor the RSA modulus.")

# Calculate Euler's totient and the private exponent
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)

# Decrypt each character
plaintext = "".join(
    chr(pow(value, d, n)) for value in ciphertext
)

print("Factor p:", p)
print("Factor q:", q)
print("Totient phi(n):", phi)
print("Private exponent d:", d)
print("Recovered flag:", plaintext)
