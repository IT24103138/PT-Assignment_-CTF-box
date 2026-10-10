from pathlib import Path

shift = 7
source = Path("memo_plaintext.txt")
output = Path("intercepted_memo.txt")


def caesar_encrypt(text, shift):
    result = []

    for char in text:
        if "A" <= char <= "Z":
            result.append(
                chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
            )
        elif "a" <= char <= "z":
            result.append(
                chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
            )
        else:
            result.append(char)

    return "".join(result)


plaintext = source.read_text(encoding="utf-8")
ciphertext = caesar_encrypt(plaintext, shift)
output.write_text(ciphertext, encoding="utf-8")

print("Encryption completed.")
print(f"Encrypted challenge saved to: {output}")
print("Keep memo_plaintext.txt private.")
