import requests
import json
import time
import os

from datetime import datetime


# Hacker News API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Required header for API requests
HEADERS = {
    "User-Agent": "TrendPulse/1.0"
}


# Categories and the keywords used to identify them
CATEGORIES = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],

    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],

    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game",
        "team", "player", "league", "championship"
    ],

    "science": [
        "research", "study", "space", "physics",
        "biology", "discovery", "NASA", "genome"
    ],

    "entertainment": [
        "movie", "film", "music", "Netflix",
        "game", "book", "show", "award", "streaming"
    ]
}


# Fetch the first 500 top story IDs
def fetch_top_story_ids():
    try:
        response = requests.get(
            TOP_STORIES_URL,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        story_ids = response.json()

        return story_ids[:500]

    except requests.RequestException as error:
        print("Could not fetch top stories:", error)
        return []


# Fetch details of one Hacker News story
def fetch_story(story_id):
    url = ITEM_URL.format(story_id)

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:
        print(f"Could not fetch story {story_id}: {error}")
        return None


# Fetch details for all the story IDs
def fetch_all_stories(story_ids):
    all_stories = []

    for index, story_id in enumerate(story_ids, start=1):

        story = fetch_story(story_id)

        # Only save the story if the API request was successful
        if story is not None:
            all_stories.append(story)

        # Show progress after every 50 stories
        if index % 50 == 0:
            print(f"Fetched {index} out of {len(story_ids)} stories")

    return all_stories


# Categorize stories based on keywords
def collect_stories(all_stories):
    collected_stories = []

    # Used to prevent the same story from appearing in multiple categories
    used_ids = set()

    category_counts = {}

    # Process one category at a time
    for category, keywords in CATEGORIES.items():

        category_count = 0

        for story in all_stories:

            # Stop once 25 stories are collected for this category
            if category_count >= 25:
                break

            story_id = story.get("id")

            # Skip stories that were already assigned another category
            if story_id in used_ids:
                continue

            title = story.get("title", "")

            # Check every keyword for the current category
            for keyword in keywords:

                if keyword.lower() in title.lower():

                    # Store only the fields required by the task
                    formatted_story = {
                        "post_id": story_id,
                        "title": title,
                        "category": category,
                        "score": story.get("score", 0),
                        "num_comments": story.get("descendants", 0),
                        "author": story.get("by", "unknown"),
                        "collected_at": datetime.now().isoformat()
                    }

                    collected_stories.append(formatted_story)

                    used_ids.add(story_id)

                    category_count += 1

                    # Stop checking more keywords once the story matches
                    break

        category_counts[category] = category_count

        print(f"{category}: {category_count} stories")

        # Required by the assignment:
        # wait once after processing each category
        time.sleep(2)

    return collected_stories, category_counts


# Save collected stories into a JSON file
def save_to_json(stories):

    # Create data folder if it does not already exist
    os.makedirs("data", exist_ok=True)

    # Today's date in YYYYMMDD format
    current_date = datetime.now().strftime("%Y%m%d")

    file_path = f"data/trends_{current_date}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            stories,
            file,
            indent=4,
            ensure_ascii=False
        )

    return file_path


def main():

    print("Fetching top Hacker News story IDs...")

    story_ids = fetch_top_story_ids()

    if not story_ids:
        print("No story IDs were fetched.")
        return

    print(f"Fetched {len(story_ids)} story IDs.")

    print("\nFetching story details...")

    all_stories = fetch_all_stories(story_ids)

    print(f"\nSuccessfully fetched {len(all_stories)} story details.")

    print("\nCategorizing stories...")

    collected_stories, category_counts = collect_stories(all_stories)

    print("\nCategory counts:")

    for category, count in category_counts.items():
        print(f"{category}: {count}")

    file_path = save_to_json(collected_stories)

    print(
        f"\nCollected {len(collected_stories)} stories. "
        f"Saved to {file_path}"
    )


if __name__ == "__main__":
    main()
