import json
import os
import urllib.request
from pathlib import Path

base = Path(__file__).resolve().parent.parent / "ctfd" / "challenges"

with open(base / "challenges.json", encoding="utf-8") as f:
    challenges = json.load(f)

with open(base / "flags.json", encoding="utf-8") as f:
    flags = json.load(f)

url = os.environ.get("CTFD_URL", "http://127.0.0.1:8000").rstrip("/")
token = os.environ.get("CTFD_ADMIN_TOKEN")

if not token:
    raise SystemExit("Please set CTFD_ADMIN_TOKEN first.")

headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json",
}

for challenge in challenges:
    payload = {
        "name": challenge["name"],
        "description": challenge["description"],
        "value": challenge["value"],
        "category": challenge["category"],
        "type": "standard",
        "state": challenge["state"],
    }

    request = urllib.request.Request(
        f"{url}/api/v1/challenges",
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        result = json.load(response)

    new_id = result["data"]["id"]

    for flag in flags:
        if flag["challenge_id"] == challenge["id"]:
            flag_payload = {
                "challenge_id": new_id,
                "type": flag["type"],
                "content": flag["content"],
                "data": flag["data"],
            }

            flag_request = urllib.request.Request(
                f"{url}/api/v1/flags",
                data=json.dumps(flag_payload).encode(),
                headers=headers,
                method="POST",
            )

            with urllib.request.urlopen(flag_request):
                pass

    print(f"Imported: {challenge['name']}")

print("CTFd challenges imported successfully.")
