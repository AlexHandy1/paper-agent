#next steps
    #explore adding other sources / extending searches (e.g. more terms, more platforms?)
    #setup cronjobs based on target terms / platforms (e.g. so work like automated alerts)

import article_consolidator as ac
import llm_reviewer as lr
from utils import * 
import datetime
from datetime import datetime
import faiss
from sentence_transformers import SentenceTransformer
import sys
import config as cf

system_prompt = "You are an expert scientific reviewer that reviews and summarises scientific text in an unbiased, scholarly tone"
llm_agent = lr.LLMReviewer(system_prompt)

today = datetime.now()
today_str = today.strftime("%d_%m_%Y_%H_%M_%S")

query = sys.argv[1]
topic_keyword = sys.argv[2]
print("Query: ", query)
print("Topic check: ", topic_keyword)

max_results = 10
article_consolidator = ac.ArticleConsolidator(query, max_results, min_date='2020/01/01', search_date=today_str)
articles = article_consolidator.consolidate()

labelled_articles = []

#get existing titles to prevent duplicates
credentials_key_path = cf.setup_config["credentials_key_path"]
gsheet_key = cf.setup_config["gsheet_key"]
gsheet_tab_name = 'To Read - AgentList'
tgt_col_num = 1

current_paper_titles = get_worksheet_title_list(gsheet_key, credentials_key_path, gsheet_tab_name, tgt_col_num)


# Print the consolidated articles
for article in articles:
    print("Title: ", article['Title'])
    print("Abstract: ", article['Abstract'])
    print("Published: ", article['Published'])
    print("Link: ", article['Link'])
    print("Source: ", article['Source'])

    if article["Title"] in current_paper_titles:
        print("Not added: article title already in list")
    else:
        #review the content with ChatGPT
        llm_topic_mention_prompt_template = """ 

        Does the abstract below mention {topic}?

        If the answer is yes, please respond with "Yes: <Example sentence that mentions topic>"
        If the answer is no, please respond with "No"

        {abstract}

        """
        llm_topic_mention_prompt = llm_topic_mention_prompt_template.format(topic=topic_keyword, abstract=article['Abstract'])
        llm_topic_review = llm_agent.chat_without_memory(llm_topic_mention_prompt)
        print("LLM Agent topic review: ", llm_topic_review)
        print('-' * 80)
        article["Topic Check"] = llm_topic_review
        article["Topic Check Query"] = topic_keyword
        labelled_articles.append(article)

add_articles_to_gsheet(labelled_articles, gsheet_key, credentials_key_path, gsheet_tab_name)