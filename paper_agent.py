#next steps
    #add bioxriv, medxriv (and google scholar)
    #try other LLMs

import article_consolidator as ac
import llm_reviewer as lr
from utils import * 
import datetime
from datetime import datetime
import sys
import config as cf

system_prompt = "You are an expert scientific reviewer that reviews and summarises scientific text in an unbiased, scholarly tone"
llm_agent = lr.LLMReviewer(system_prompt)

today = datetime.now()
today_str = today.strftime("%d_%m_%Y_%H_%M_%S")

queries = cf.query_config["queries"]
queries_topic_checks = cf.query_config["topic_checks"]
max_results = cf.query_config["max_results"]
search_sources = cf.query_config["search_sources"]

run_topic_check = cf.llm_config["run_topic_check"]

for idx, query in enumerate(queries):
    print("Query: ", query)
    article_consolidator = ac.ArticleConsolidator(query, max_results, min_date='2020/01/01', search_date=today_str, search_sources=search_sources)
    articles = article_consolidator.consolidate()

    labelled_articles = []

    #get existing titles to prevent duplicates
    credentials_key_path = cf.setup_config["credentials_key_path"]
    gsheet_key = cf.setup_config["gsheet_key"]
    gsheet_tab_name = cf.setup_config["gsheet_tab_name"]
    tgt_col_num = cf.setup_config["target_col_num"]

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
        elif run_topic_check:
            query_topic_check = queries_topic_checks[idx]
            print("Query topic check: ", query_topic_check)

            #review the content with ChatGPT
            llm_topic_mention_prompt_template = """ 

            Does the abstract below mention {topic}?

            If the answer is yes, please respond with "Yes: <Example sentence that mentions topic>"
            If the answer is no, please respond with "No"

            {abstract}

            """
            llm_topic_mention_prompt = llm_topic_mention_prompt_template.format(topic=query_topic_check, abstract=article['Abstract'])
            llm_topic_review = llm_agent.chat_without_memory(llm_topic_mention_prompt)
            print("LLM Agent topic review: ", llm_topic_review)
            print('-' * 80)
            article["Topic Check"] = llm_topic_review
            article["Topic Check Query"] = query_topic_check
            labelled_articles.append(article)
        else:
            print("Topic check query not run")
            article["Topic Check"] = "N/A"
            article["Topic Check Query"] = "N/A"
            labelled_articles.append(article)

    add_articles_to_gsheet(labelled_articles, gsheet_key, credentials_key_path, gsheet_tab_name)