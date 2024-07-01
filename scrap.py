# scrap.py

import sys
import requests
from bs4 import BeautifulSoup
import json

def get_category_count(category):
    url = 'https://es.scalperscompany.com'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Example selectors, adjust these according to the actual website structure
    if category == 'jeans':
        elements = soup.find_all(class_='category-jeans')
    elif category == 'shirts':
        elements = soup.find_all(class_='category-shirts')
    else:
        print(f"Invalid category: {category}")
        sys.exit(1)
    
    return len(elements)

def main():
    if len(sys.argv) != 2:
        print("Usage: python scrap.py <category>")
        sys.exit(1)
    
    category = sys.argv[1]
    count = get_category_count(category)
    
    result = {
        'category': category,
        'count': count
    }
    
    with open('find.json', 'w') as f:
        json.dump(result, f)

if __name__ == "__main__":
    main()
