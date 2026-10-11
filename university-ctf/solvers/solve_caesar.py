
from pathlib import Path

# Find the project folders relative to this script
BASE_DIR = Path(__file__).resolve().parent
ciphertext_file = BASE_DIR.parent / "crypto01" / "intercepted_memo.txt"

# Read the encrypted message
ciphertext = ciphertext_file.read_text(encoding="utf-8")


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


# Try every possible Caesar shift
for shift in range(26):
    print(f"\n--- Shift {shift} ---")
    print(caesar_decrypt(ciphertext, shift))
