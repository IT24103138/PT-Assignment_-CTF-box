
# CRYPTO-02: Weak Lock, Strong Guess
# Educational RSA decryption demonstration

n = 3233
e = 17

ciphertext = [
    641, 2159, 325, 855, 1107, 1313,
    1632, 690, 119, 2412, 1230, 1632,
    119, 1773, 1313, 2271, 2185, 1516
]

# Factor the deliberately small RSA modulus
p = 61
q = 53

print("RSA Challenge: Weak Lock, Strong Guess")
print(f"Public modulus n = {n}")
print(f"Public exponent e = {e}")
print(f"Factors: p = {p}, q = {q}")

# Calculate Euler's totient
phi = (p - 1) * (q - 1)

# Calculate the private exponent
d = pow(e, -1, phi)

print(f"Totient phi(n) = {phi}")
print(f"Private exponent d = {d}")

# Decrypt each ciphertext integer
plaintext = "".join(
    chr(pow(value, d, n)) for value in ciphertext
)

print("\nDecrypted message:")
print(plaintext)
