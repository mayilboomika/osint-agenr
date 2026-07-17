from investigate import investigate
from services import search_topic


# Investigation topic
topic = input("Enter investigation topic: ").strip()

# Search for the topic
search_data = search_topic(topic)
sources = search_data.get("sources", [])

# Generate prompt
report = investigate(search_data.get("topic", topic), sources)


# Display prompt
print("\n========== INVESTIGATION REPORT ==========\n")
print(report)