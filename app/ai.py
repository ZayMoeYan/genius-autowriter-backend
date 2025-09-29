import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY is missing in .env")

client = genai.Client(api_key=API_KEY)

def generate_content(prompt: str, images: list[tuple[bytes, str]] = None) -> str:
    try:
        parts = [{"text": prompt}]

        if images:
            for image_bytes, mime_type in images:
                parts.append({
                    "inline_data": {
                        "mime_type": mime_type,
                        "data": image_bytes 
                    }
                })

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[parts]
        )
        return response.text.strip()
    except Exception as e:
        raise e
