from pathlib import Path

ciphertext = Path(
    "../crypto01/intercepted_memo.txt"
).read_text()


def caesar_decrypt(text, shift):
    result = []

    for char in text:
        if "A" <= char <= "Z":
            result.append(
                chr((ord(char) - ord("A") - shift) % 26 + ord("A"))
            )
        elif "a" <= char <= "z":
            result.append(
                chr((ord(char) - ord("a") - shift) % 26 + ord("a"))
            )
        else:
            result.append(char)

    return "".join(result)


for shift in range(26):
    print(f"\n--- Shift {shift} ---")
    print(caesar_decrypt(ciphertext, shift))
