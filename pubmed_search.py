import requests
import xml.etree.ElementTree as ET

class PubMedSearch:
    def __init__(self, query, max_results=10, min_date='2020/01/01'):
        self.query = query
        self.max_results = max_results
        self.min_date = min_date
        self.base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
        self.search_url = self.base_url + 'esearch.fcgi'
        self.fetch_url = self.base_url + 'efetch.fcgi'

    def search(self):
        params = {
            'db': 'pubmed',
            'term': self.query,
            'retmode': 'xml',
            'retmax': self.max_results,
            'sort': 'pubdate',
            'mindate': self.min_date
        }

        # Make a request to the PubMed API to retrieve the list of article IDs
        response = requests.get(self.search_url, params=params)

        # Parse the XML response using ElementTree
        root = ET.fromstring(response.content)
        id_list = [id_elem.text for id_elem in root.findall('.//Id')]

        # Make a request to the PubMed API to retrieve the abstract for each article
        articles = []
        for article_id in id_list:
            fetch_params = {
                'db': 'pubmed',
                'id': article_id,
                'retmode': 'xml',
                'rettype': 'abstract', 
                'pubdate': 'Y'
            }
            fetch_response = requests.get(self.fetch_url, params=fetch_params)

            # Parse the XML response using ElementTree
            fetch_root = ET.fromstring(fetch_response.content)
            article_elem = fetch_root.find('.//PubmedArticle')
            title_elem = article_elem.find('.//ArticleTitle')
            title = title_elem.text if title_elem is not None else ''
            abstract_elem = article_elem.find('.//AbstractText')
            abstract = abstract_elem.text if abstract_elem is not None else ''

            pubdate_elem = article_elem.find('.//PubDate') 
            pubdate = ''
            year_elem = pubdate_elem.find('.//Year')
            year = year_elem.text if year_elem is not None else ''
            month_elem = pubdate_elem.find('.//Month') 
            month = month_elem.text if month_elem is not None else ''
            day_elem = pubdate_elem.find('.//Day')
            day = day_elem.text if day_elem is not None else ''
            pubdate = f'{year}-{month}-{day}'

            url_elem = article_elem.find('.//ArticleId[@IdType="pubmed"]')
            url = f'https://pubmed.ncbi.nlm.nih.gov/{url_elem.text}' if url_elem is not None else ''

            article = {
                'title': title,
                'abstract': abstract,
                'pubdate': pubdate, 
                'link': url
            }
            
            articles.append(article)

        return articles
