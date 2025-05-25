import requests
from bs4 import BeautifulSoup

def get_wikipedia_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        return response.text
    
    except requests.RequestEception as e:
        print(f"Error: {e}")


def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')