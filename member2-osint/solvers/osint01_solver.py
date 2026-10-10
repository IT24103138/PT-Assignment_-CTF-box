import re
import subprocess
import requests

BASE = "http://localhost:8081"

# Step 1: read the staff directory and find the email pattern
page = requests.get(BASE + "/").text
emails = re.findall(r"[a-z.]+@campus-it\.local", page)
print("Emails found:", emails)

# Step 2: read the paste page and find the image path
paste = requests.get(BASE + "/paste/p4x91.html").text
image_path = re.findall(r"/files/\S+\.jpg", paste)[0]
print("Image path:", image_path)

# Step 3: download the image
img = requests.get(BASE + image_path)
open("badge.jpg", "wb").write(img.content)
print("Image downloaded")

# Step 4: read the metadata and pull out the flag
result = subprocess.run(["exiftool", "badge.jpg"], capture_output=True, text=True)
flag = re.findall(r"FLAG\{.*?\}", result.stdout)[0]
print("FLAG:", flag)
