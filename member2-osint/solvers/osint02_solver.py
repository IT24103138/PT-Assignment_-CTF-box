import re
import subprocess
import tempfile

URL = "http://localhost:3000/ctfadmin/it-club-portal.git"

# Step 1: clone the repo into a temporary folder
folder = tempfile.mkdtemp()
subprocess.run(["git", "clone", URL, folder], check=True)

# Step 2: read the whole history and find the flag
history = subprocess.run(["git", "log", "--all", "-p"], cwd=folder,
                         capture_output=True, text=True).stdout
flag = re.findall(r"FLAG\{.*?\}", history)[0]
print("FLAG:", flag)

# Step 3: find which commit first added the flag
hashes = subprocess.run(["git", "log", "--format=%h"], cwd=folder,
                        capture_output=True, text=True).stdout.split()
hashes.reverse()  # oldest commit first
for h in hashes:
    shown = subprocess.run(["git", "show", h], cwd=folder,
                           capture_output=True, text=True).stdout
    if flag in shown:
        print("Flag first appeared in commit:", h)
        break
