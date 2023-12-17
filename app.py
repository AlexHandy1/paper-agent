import article_consolidator as ac
import config as cf
import datetime
from datetime import datetime
import llm_reviewer as lr
import pickle
from sentence_transformers import SentenceTransformer
import sys
from utils import * 

def lambda_handler(event, context):
	print(event)
	today = datetime.now()
	today_str = today.strftime("%d_%m_%Y_%H_%M_%S")
	print("Running at: ", today_str)

	queries = cf.query_config["queries"]
	queries_topic_checks = cf.query_config["topic_checks"]
	max_results = cf.query_config["max_results"]
	search_sources = cf.query_config["search_sources"]

	run_topic_check = cf.llm_config["run_topic_check"]
	run_relevance_model = cf.llm_config["run_relevance_model"]
	relevance_model_encoder_filepath = cf.llm_config["run_relevance_model_encoder_path"]
	relevance_model_filepath = cf.llm_config["run_relevance_model_path"]

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

	        #filter model logic could be added here (e.g. elif relevance==N, print("Model judges not relevant, filter out"))

	        if article["Title"] in current_paper_titles:
	            print("Not added: article title already in list")
	        #handle empty cases
	        elif (article["Title"] == "") | (article["Title"] == " ") | (article["Title"] == None):
	            print("Not added: empty article title")
	        else: 
	            if run_topic_check:
	                system_prompt = "You are an expert scientific reviewer that reviews and summarises scientific text in an unbiased, scholarly tone"
	                llm_agent = lr.LLMReviewer(system_prompt)
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
	                # labelled_articles.append(article)
	            else:
	                print("Topic check query not run")
	                article["Topic Check"] = "N/A"
	                article["Topic Check Query"] = "N/A"
	                # labelled_articles.append(article)

	            if run_relevance_model:
	                print("Relevance model running")
	                #load models
	                relevance_model = pickle.load(open(relevance_model_filepath, 'rb'))
	                # encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
	                encoder = SentenceTransformer(relevance_model_encoder_filepath)

	                #generate title embeddings
	                title_vector = encoder.encode(article['Title'])

	                #generate prediction
	                relevance_pred_raw = relevance_model.predict(title_vector.reshape(1, -1))
	                print("Relevance raw pred: ", relevance_pred_raw)

	                #convert prediction into format
	                relevance_pred = parse_relevance_pred(relevance_pred_raw)
	                print("Relevance pred: ", relevance_pred)

	                #fill in dict
	                article["Relevant_pred"] = relevance_pred
	            else:
	                print("Relevance model not run")
	                article["Relevant_pred"] = "TBD"


	            labelled_articles.append(article)

	    add_articles_to_gsheet(labelled_articles, gsheet_key, credentials_key_path, gsheet_tab_name)


	return {
		"statusCode": 200,
		"body": "Hello from Lambda Container Images!"
	}

