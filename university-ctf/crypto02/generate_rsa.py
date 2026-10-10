from pathlib import Path

# Deliberately small values for this classroom exercise
p = 61
q = 53
n = p * q
e = 17

flag = "CTF{weak_rsa_demo}"

# Educational example: encrypt each character separately
ciphertext = [pow(ord(char), e, n) for char in flag]

challenge = (
    f"n = {n}\n"
    f"e = {e}\n"
    f"c = {ciphertext}\n"
)

Path("rsa_challenge.txt").write_text(challenge)

print("RSA challenge file created.")
print(challenge)
