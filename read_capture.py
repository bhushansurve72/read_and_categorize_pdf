import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-pro-vision")

def analyze_image_google(image_path):
    with open(image_path, "rb") as f:
        img_data = f.read()

    response = model.generate_content([
        "Extract name, address, city, state, zipcode as JSON.", 
        {"mime_type": "image/png", "data": img_data}
    ])

    
    return response.text
