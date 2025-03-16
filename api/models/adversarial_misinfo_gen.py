import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_adversarial_misinformation(topic, bias):
    """ Generates biased misinformation on a given topic """
    prompt = f"Generate a misleading news headline and article about {topic} with a {bias} bias."

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]
