import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def extract_entities_gpt(text):
    prompt = f"Extract named entities (persons, organizations, locations) from:\n\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

def detect_stance_gpt(claim, text):
    prompt = f"Analyze the stance of the following text towards the claim: '{claim}'.\n\n{text}\n\nClassify as: [support, neutral, against]."
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]
