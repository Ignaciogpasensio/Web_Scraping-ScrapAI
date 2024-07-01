# find.py

import sys
import requests
from bs4 import BeautifulSoup
import json

def get_category_count(category):
    url = 'https://es.scalperscompany.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the quantity of the selected category in the website
    # This part needs to be adjusted based on the actual HTML structure of the Scalpers website
    # For demonstration, we will assume there are HTML elements with specific classes or IDs for jeans and shirts

    if category == 'jeans':
        elements = soup.find_all(class_='category-jeans')
    elif category == 'shirts':
        elements = soup.find_all(class_='category-shirts')
    else:
        return 0
    
    return len(elements)

def main():
    if len(sys.argv) != 2:
        print("Usage: python find.py <category>")
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
