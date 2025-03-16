import json
import spacy
from transformers import pipeline

# Load a pre-trained NER model from spaCy
nlp = spacy.load("en_core_web_sm")

# Load a pre-trained stance detection model (zero-shot classification)
stance_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Load JSON files
def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []

# Extract entities using spaCy
def extract_entities(text):
    if not text:  # Ensure text is valid
        return []
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

# Perform stance detection safely
def detect_stance(claim, text):
    if not text or not isinstance(text, str):  # Ensure text is a valid string
        return "Unknown"
    result = stance_classifier(text.strip(), [claim], multi_label=False)
    return result["labels"][0]  # Returns the most likely stance

# Load JSON files safely
news_data = load_json("scraped_news.json")
reddit_data = load_json("reddit_conspiracy.json")

# Merge both datasets
merged_data = news_data + reddit_data
print(f" Merged {len(news_data)} news articles & {len(reddit_data)} Reddit posts.")

# Process each entry
for i, item in enumerate(merged_data):
    text = item.get("headline") or item.get("text")  # Use headline for news, text for Reddit
    text = text if isinstance(text, str) else ""  # Ensure text is a string

    if not text.strip():  # Skip empty text
        item["entities"] = []
        item["stance"] = "Unknown"
    else:
        item["entities"] = extract_entities(text)
        item["stance"] = detect_stance("COVID-19 vaccines are effective.", text)

    if i % 10 == 0:  # Print progress every 10 items
        print(f"Processed {i+1}/{len(merged_data)}")

# Save processed data
output_file = "processed_data.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(merged_data, f, indent=4)

print(f" JSON files merged and processed successfully! Saved to {output_file}.")
