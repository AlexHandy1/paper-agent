import re
import pandas as pd

with open('weekly_papers_2021_2023_vtoread.txt', 'r') as f:
    text = f.read()

articles_to_read = []
matches = re.findall(r'\d+\. (.+?) - (https?://\S+)', text)
for match in matches:
	entry = {}
	title = match[0]
	link = match[1]
	print(f'<TITLE>{title}<TITLE> - <LINK>{link}<LINK>')
	entry["title"] = title
	entry["link"] = link
	articles_to_read.append(entry)

articles_to_read_df = pd.DataFrame(articles_to_read)
articles_to_read_df.to_csv('articles_to_read_12052023.csv', index=False)