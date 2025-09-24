import streamlit as st
import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()
# 🔑 Configure Gemini API key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

for model in genai.list_models():
    print(model.name, model.supported_generation_methods)

# Load Gemini Vision model
model = genai.GenerativeModel("gemini-2.0-flash")

st.title("📄 Handwritten OCR with Google Gemini Vision")

uploaded_file = st.file_uploader("Upload handwritten document", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Save uploaded file
    file_path = "temp_upload.png"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(file_path, caption="Uploaded Image", use_column_width=True)

    if st.button("Extract Data"):
        with st.spinner("Analyzing image with Gemini Flash..."):
            with open(file_path, "rb") as f:
                img_data = f.read()

            # Ask Gemini to extract structured JSON
            prompt = """
            You are an OCR engine. Read the uploaded document image
            and Return ONLY valid JSON in the following structure, no explanations, no extra text::
            {
                "request_type": "address change",
                "current_address": {
                    "street": "...",
                    "city": "...",
                    "state": "...",
                    "zipcode": "..."
                },
                "new_address": {
                    "street": "...",
                    "city": "...",
                    "state": "...",
                    "zipcode": "..."
                },
                "start_date": "YYYY-MM-DD"
                }
            """

            response = model.generate_content([
                prompt,
                {"mime_type": "image/png", "data": img_data}
            ])

            text_response = response.text.strip()

            # Try to extract JSON block safely
            match = re.search(r"\{.*\}", text_response, re.DOTALL)
            if match:
                json_str = match.group(0)
                try:
                    parsed = json.loads(json_str)
                    st.subheader("📝 Extracted Data")
                    st.json(parsed)
                except json.JSONDecodeError as e:
                    st.error(f"JSON parsing failed: {e}")
                    st.code(json_str)
            else:
                st.error("No JSON object found in the response.")
                st.code(text_response)
