import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import json

def crawl_page(page_number, results):
    url = f'https://books.toscrape.com/catalogue/page-{page_number}.html'
    response = requests.get(url)
    if response.status_code != 200:
        return
         
    soup = BeautifulSoup(response.text, 'html.parser')
    books = []
    for book in soup.find_all('article', class_='product_pod'):
        title = book.find('h3').find('a').get('title')
        price = book.find('p', class_='price_color').text.strip().replace('Â', '')
        rating_class = book.find('p', class_='star-rating')['class']

        if rating_class[1] == 'Five':
            books.append({"title": title, "price": price})
    
    if page_number in results:
        results[page_number] += books
    else:
        results[page_number] = books

def main():
    max_pages = 4
    output_file = 'five_star_books.json'
    results = {}

    with ThreadPoolExecutor(max_workers=4) as executor:
        for page_number in range(1, max_pages + 1):
            executor.submit(crawl_page, page_number, results)
            
    sorted_results = dict(sorted(results.items()))

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(sorted_results, file, indent=4, ensure_ascii=False)
    
if __name__ == '__main__':
    main()
