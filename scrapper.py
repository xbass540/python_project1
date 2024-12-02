from bs4 import BeautifulSoup
import requests

with open('test_html.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

for article in soup.find_all('div',class_='article'):
    headline = article.a.h1.text
    summary = article.p.text
    print(headline)
    print(summary)
    print()
