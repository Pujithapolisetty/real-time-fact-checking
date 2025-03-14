import praw
import json

# ✅ Ensure you have correct API credentials from https://www.reddit.com/prefs/apps/
reddit = praw.Reddit(
    client_id="UKq6xXFIQGgRIyVt_Gia-Q",       # Your actual Client ID
    client_secret="ZguWOyD7fF1nCpVP-SQ-beYiLKrL9g",  # Your actual Client Secret
    user_agent="SentimentAnalyzerBot/1.0 by Complex-Standard238",
    username="Complex-Standard238",   # Replace with your Reddit username
    password="Pujitha@7036"    # Replace with your Reddit password
)
def scrape_reddit(subreddit="conspiracy", limit=10):
    """Scrapes top posts from a subreddit."""
    posts = []
    
    try:
        for post in reddit.subreddit(subreddit).hot(limit=limit):
            posts.append({
                "title": post.title,
                "author": post.author.name if post.author else "Unknown",
                "timestamp": post.created_utc,
                "url": post.url,
                "score": post.score,
                "num_comments": post.num_comments
            })

        # Save data to JSON file
        with open(f"reddit_{subreddit}.json", "w", encoding="utf-8") as file:
            json.dump(posts, file, indent=4)

        print(f"✅ Saved {len(posts)} posts from r/{subreddit}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    scrape_reddit("conspiracy", limit=10)
