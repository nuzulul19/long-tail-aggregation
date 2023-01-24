import requests
import urllib
from requests_html import HTMLSession


def _get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)


def scrape_google(query):
    """Scrape url data from google"""
    query = urllib.parse.quote_plus(query)
    response = _get_source("https://www.google.co.id/search?q=" + query)

    print("scrapping url from google with search query:", query)
    links = list(response.html.absolute_links)
    google_domains = (
        "https://www.google.",
        "https://google.",
        "https://webcache.googleusercontent.",
        "http://webcache.googleusercontent.",
        "https://policies.google.",
        "https://support.google.",
        "https://maps.google.",
    )

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)

    return links
