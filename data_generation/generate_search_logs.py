import csv
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

NUM_EVENTS = 10000
NUM_USERS = 1000
OUTPUT_PATH = "data/raw/search_logs/search_logs.csv"


QUERIES = [
    "best laptop 2024", "how to learn python", "weather today",
    "online shopping deals", "recipe for pasta", "netflix movies",
    "flight tickets cheap", "gym near me", "news today",
    "iphone review", "how to lose weight", "jobs remote",
    "youtube trending", "amazon prime", "hotels in paris",
    "bitcoin price", "spotify playlist", "coffee shops nearby",
    "best restaurants", "car insurance quotes", "stock market",
    "travel destinations", "gaming laptop", "healthy recipes",
    "workout at home", "streaming services", "book recommendations"
]

DEVICES = ["mobile", "desktop", "tablet"]
COUNTRIES = ["United States", "United Kingdom", "India", "Germany", "Canada", "France", "Australia", "Brazil"]
BROWSERS = ["Chrome", "Safari", "Firefox", "Edge"]
DOMAINS = ["google.com", "amazon.com", "youtube.com", "wikipedia.org", "reddit.com", "medium.com", "yelp.com"]


def generate_event(user_id, session_id, timestamp):
    query = random.choice(QUERIES)
    clicked = random.random() < 0.65  
    
    return {
        "event_id": str(uuid.uuid4()),
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": user_id,
        "session_id": session_id,
        "query": query,
        "clicked": clicked,
        "clicked_url": f"https://{random.choice(DOMAINS)}/{query.replace(' ', '-')}" if clicked else None,
        "clicked_position": random.randint(1, 10) if clicked else None,
        "device": random.choice(DEVICES),
        "browser": random.choice(BROWSERS),
        "country": random.choice(COUNTRIES),
        "results_count": random.randint(100, 5000)
    }


def main():
    print(f"Generating {NUM_EVENTS:,} search events...")
    
   
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    

    output_path = project_root / OUTPUT_PATH
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    
    events = []
    start_date = datetime.now() - timedelta(days=30)
    
    for i in range(NUM_EVENTS):
        user_id = f"user_{random.randint(1, NUM_USERS):04d}"
        session_id = f"sess_{uuid.uuid4().hex[:8]}"
        timestamp = start_date + timedelta(seconds=random.randint(0, 30 * 24 * 3600))
        
        events.append(generate_event(user_id, session_id, timestamp))
    
    
    events.sort(key=lambda x: x["timestamp"])
    
    
    fieldnames = ["event_id", "timestamp", "user_id", "session_id", "query", 
                  "clicked", "clicked_url", "clicked_position", "device", 
                  "browser", "country", "results_count"]
    
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(events)
    
    print(f"Done! Saved to {output_path}")
    print(f"File size: {output_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()

