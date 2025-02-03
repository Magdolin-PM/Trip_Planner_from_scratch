import json
import os
from typing import List, Dict, Any
import requests
from langchain_core.tools import tool


class SearchTools:
    def __init__(self):
        self.api_key = os.getenv('SERPER_API_KEY')
        if not self.api_key:
            raise ValueError("SERPER_API_KEY environment variable is not set")

    @tool("Search the internet")
    def search_internet(self, query: str) -> List[Dict[str, Any]]:
        """Useful to search the web for information about a specific topic and return results in a structured format"""
        top_result_to_return = 4
        url = "https://google.serper.dev/search"
        
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            search_results = response.json()
            
            results = []
            if 'organic' in search_results:
                for result in search_results['organic'][:top_result_to_return]:
                    results.append({
                        'title': result.get('title', ''),
                        'link': result.get('link', ''),
                        'snippet': result.get('snippet', '')
                    })
            
            return results
            
        except requests.exceptions.RequestException as e:
            return [{"error": f"Search failed: {str(e)}"}]
            
    def search_internet_old(self, query):
        return f"Search results for: {query}"
            