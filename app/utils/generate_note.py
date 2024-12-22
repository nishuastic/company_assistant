import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_note(request):
    prompt = f"""
    Write a LinkedIn connection request message based on the following details:
    - Recipient's Name: {request.recipient_name}
    - Recipient's Headline: {request.recipient_headline}
    - Recipient's About Section: {request.recipient_about}
    - Purpose of Connection: {request.purpose}
    - Sender's Name: {request.sender_name}
    The message should be polite, concise, and professional.
    """
    try:
        response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=500,
        temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating note: {str(e)}")
