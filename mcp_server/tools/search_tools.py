import requests
from bs4 import BeautifulSoup

def duckduckgo_search(query: str, max_results: int = 5) -> list:
    """
    Perform a DuckDuckGo search using the HTML endpoint and return results.

    Args:
        query (str): Search query string.
        max_results (int): Maximum number of results to return.

    Returns:
        List[dict]: List of search result dictionaries with 'title' and 'link'.
    """
    url = "https://html.duckduckgo.com/html/"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"q": query}
    
    response = requests.post(url, data=params, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for result in soup.find_all("a", class_="result__a", limit=max_results):
        title = result.get_text()
        link = result.get("href")
        results.append({"title": title, "link": link})
    
    return results
