import re
import pandas as pd

with open('weekly_papers_2021_2023_vread.txt', 'r') as f:
    lines = f.readlines()

article_list = []
title_regex = re.compile(r'(.+?) - (https?://\S+)')
title_notes_regex = re.compile(r'\* (.*)')
current_title = ""
current_notes = []

for line in lines:
    # Check if line contains a title
    title_match = title_regex.search(line)
    if title_match:
        # If we were processing notes, store them in the previous entry and reset the notes list
        if current_notes:
            entry["notes"] = ", ".join(current_notes)
            current_notes = []
            article_list.append(entry)

        # Store the current title and create a new entry
        current_title = title_match.group(1)
        entry = {"title": current_title, "url": title_match.group(2)}

    # Check if line contains notes and we are currently processing a title
    elif current_title and "*" in line:
        notes_match = title_notes_regex.search(line)
        if notes_match:
            current_notes.append(notes_match.group(1))

# Store the notes for the last entry
if current_notes:
    entry["notes"] = ", ".join(current_notes)
    article_list.append(entry)

# Create a DataFrame and save to a CSV file
article_df = pd.DataFrame(article_list)
article_df.to_csv("articles-read-11052023.csv")