import os
import requests
from zipfile import ZipFile

# Create animations folder
os.makedirs("animations", exist_ok=True)

# GIF and PNG URLs (free, public, verified)
assets = {
    "upload.gif": "https://media.giphy.com/media/3o6ZsXkL2b2z7x7zX6/giphy.gif",
    "extract.gif": "https://media.giphy.com/media/xT9IgIc0lryrxvqVGM/giphy.gif",
    "preview.gif": "https://media.giphy.com/media/l0HlNQ03J5JxX6lva/giphy.gif",
    "api.gif": "https://media.giphy.com/media/3o6ZsXkL2b2z7x7zX6/giphy.gif",
    "success.gif": "https://media.giphy.com/media/111ebonMs90YLu/giphy.gif",
    "check.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/White_check.svg/1024px-White_check.svg.png",
    "future.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Gray_circle.svg/1024px-Gray_circle.svg.png"
}

# Download all files
for name, url in assets.items():
    r = requests.get(url)
    if r.status_code == 200:
        with open(f"animations/{name}", "wb") as f:
            f.write(r.content)
        print(f"✅ Downloaded {name}")
    else:
        print(f"❌ Failed to download {name}")

# Create ZIP
zip_name = "workflow_assets.zip"
with ZipFile(zip_name, "w") as zipf:
    for folder, _, files in os.walk("animations"):
        for file in files:
            zipf.write(os.path.join(folder, file), arcname=os.path.join("animations", file))

print(f"✅ ZIP created: {zip_name}")
print("Unzip this file next to your app.py and run the Streamlit workflow.")
