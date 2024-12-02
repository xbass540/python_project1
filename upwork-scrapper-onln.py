from bs4 import BeautifulSoup
import requests
import csv

csv_file = open('solomon_blog.csv','w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['headline','summary','img_name'])


source = requests.get('https://www.upwork.com/nx/find-work/').text
print(source)


soup = BeautifulSoup(source,'lxml')

for article in soup.find_all('section'):

    headline = article.h3.a.text
    print(headline)
    summary = article.find('div',class_='air3-line-clamp')
    summary_text = summary.span.text()
    print(summary)


csv_file.close()