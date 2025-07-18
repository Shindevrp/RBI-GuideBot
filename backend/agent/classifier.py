import openai
from backend.core.config import settings

openai.api_key = settings.OPENAI_API_KEY

def classify_email_intent(subject: str, body: str) -> str:
    """
    Uses an LLM to classify the email's intent.
    Categories: RBI_REGULATION, NBFC_LENDING, COMBINED, OTHER.
    """
    content = f"Subject: {subject}\n\nBody: {body}"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert email classifier for an NBFC. Your task is to determine the user's intent based on the email content. "
                               "Classify the email into one of the following categories and respond with ONLY the category name: "
                               "'RBI_REGULATION' (for queries about RBI rules, compliance, guidelines), "
                               "'NBFC_LENDING' (for queries about internal lending processes, products, loan criteria), "
                               "'COMBINED' (if the query touches on both), or "
                               "'OTHER' (for anything else, like greetings or spam)."
                },
                {
                    "role": "user",
                    "content": content
                }
            ],
            temperature=0,
            max_tokens=10
        )
        classification = response.choices[0].message['content'].strip()
        return classification
    except Exception as e:
        print(f"Error during classification: {e}")
        return "OTHER"