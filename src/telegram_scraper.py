import json
import spacy
import asyncio
from telethon.sync import TelegramClient
from transformers import pipeline

# 🔹 Telegram API Credentials (Replace with yours)
API_ID = "your_api_id"
API_HASH = "your_api_hash"
PHONE_NUMBER = "your_phone_number"
GROUP_USERNAME = "group_username_here"  # Example: '@fakenewschat'

# 🔹 Initialize NLP Models
nlp = spacy.load("en_core_web_sm")
claim_detector = pipeline("text-classification", model="facebook/bart-large-mnli")

# 🔹 Connect to Telegram
client = TelegramClient("session_name", API_ID, API_HASH)

async def scrape_messages():
    """Scrape messages from a public Telegram group."""
    await client.start()
    messages = []
    
    async for msg in client.iter_messages(GROUP_USERNAME, limit=100):
        messages.append({
            "id": msg.id,
            "sender": msg.sender_id,
            "date": msg.date.strftime("%Y-%m-%d %H:%M:%S"),
            "text": msg.text
        })

    # Save messages to a JSON file
    with open("telegram_messages.json", "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Saved {len(messages)} messages from {GROUP_USERNAME}")
    return messages

def extract_fake_news(messages):
    """Extract potential misinformation claims from Telegram messages."""
    fake_news = []
    
    for msg in messages:
        doc = nlp(msg["text"])
        if len(doc.ents) > 2:  # If message has multiple named entities, it's likely a claim
            label = claim_detector(msg["text"])[0]["label"]
            if label == "Misinformation":  # Adjust based on model output
                fake_news.append(msg)

    # Save filtered claims
    with open("fake_news_claims.json", "w", encoding="utf-8") as f:
        json.dump(fake_news, f, indent=4, ensure_ascii=False)

    print(f"🚨 Detected {len(fake_news)} misinformation claims!")
    return fake_news

async def main():
    """Main function to scrape Telegram and extract fake news."""
    messages = await scrape_messages()
    extract_fake_news(messages)

# Run the script
with client:
    asyncio.run(main())
