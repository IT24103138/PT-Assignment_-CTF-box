
from pathlib import Path

# Small RSA values for an educational CTF challenge
p = 61
q = 53
n = p * q
e = 17

flag = "CTF{weak_rsa_demo}"

# Encrypt each character separately for this simplified exercise
ciphertext = [pow(ord(char), e, n) for char in flag]

challenge = (
    f"n = {n}\n"
    f"e = {e}\n"
    f"c = {ciphertext}\n"
)

Path("rsa_challenge.txt").write_text(
    challenge, encoding="utf-8"
)

print("RSA challenge created successfully.")
print("Public parameters saved in rsa_challenge.txt")
print(challenge)
