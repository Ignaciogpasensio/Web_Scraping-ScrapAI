import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = 'https://en.gb.scalperscompany.com/collections/woman-new-collection-skirts-2060'

# Send a GET request
response = requests.get(url)

if response.status_code == 200:
    # Initialize BeautifulSoup object with the response text
    soup = BeautifulSoup(response.text, 'html.parser')
else:
    print("Failed to fetch the webpage. Status code:", response.status_code)
