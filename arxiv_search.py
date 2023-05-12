import urllib, urllib.request
import xml.etree.ElementTree as ET

class ArxivSearch:
    def __init__(self, query, max_results):
        self.query = query
        self.max_results = max_results
        
    def search(self):
        # Create the API request URL
        base_url = 'https://export.arxiv.org/api/query?'
        query_params = {
            'search_query': f'all:{self.query}',
            'start': 0,
            'max_results': self.max_results,
            'sortBy': 'lastUpdatedDate',
            'sortOrder': 'descending'
        }
        url = base_url + urllib.parse.urlencode(query_params)

        # Send the request and parse the response
        data = urllib.request.urlopen(url)
        data_parsed = data.read().decode('utf-8')
        xml_data_parsed = ET.fromstring(data_parsed)

        # Extract the article data
        articles = []
        for entry in xml_data_parsed.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title')
            published = entry.find('{http://www.w3.org/2005/Atom}published')
            updated = entry.find('{http://www.w3.org/2005/Atom}updated')
            summary = entry.find('{http://www.w3.org/2005/Atom}summary')
            link = entry.find('{http://www.w3.org/2005/Atom}link[@type="text/html"][@rel="alternate"][@href]')

            article = {
                'title': title.text,
                'published': published.text,
                'updated': updated.text,
                'summary': summary.text,
                'link': link.get('href')
            }

            articles.append(article)
        
        return articles