import arxiv_search as ar
import pubmed_search as pb

class ArticleConsolidator:
    def __init__(self, query, max_results, min_date=None, search_date=None):
        self.query = query
        self.max_results = max_results
        self.min_date = min_date
        self.search_date = search_date
    
    def consolidate(self):
        pubmed_search = pb.PubMedSearch(self.query, max_results=self.max_results, min_date=self.min_date)
        pubmed_articles = pubmed_search.search()
        
        arxiv_search = ar.ArxivSearch(self.query, max_results=self.max_results)
        arxiv_articles = arxiv_search.search()
        
        articles = []
        for pubmed_article in pubmed_articles:
            articles.append({
                'Title': pubmed_article['title'],
                'Abstract': pubmed_article['abstract'],
                'Published': pubmed_article['pubdate'],
                'Link': pubmed_article['link'],
                'Source': 'PubMed', 
                'Query': self.query,
                'SearchDate': self.search_date, 
                'Category': "N/A"
            })
        
        for arxiv_article in arxiv_articles:
            articles.append({
                'Title': arxiv_article['title'],
                'Abstract': arxiv_article['summary'],
                'Published': arxiv_article['published'],
                'Link': arxiv_article['link'],
                'Source': 'Arxiv',
                'Query': self.query,
                'SearchDate': self.search_date,
                'Category': "N/A"
            })
        
        return articles