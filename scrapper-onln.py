from bs4 import BeautifulSoup
import requests
import csv

csv_file = open('solomon_blog.csv','w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['headline','summary','img_name'])

source = requests.get('https://solomondesigns.co.uk/blog').text

soup = BeautifulSoup(source,'lxml')

for article in soup.find_all('article'):


    headline = article.h2.a.text
    print(headline)
    summary = article.p.text
    print(summary)
    read_more = article.find('p',class_='read-more-container')
    read_more_btn = read_more.a.text

    print(read_more_btn)
    #print(article.prettify())
    try:
        img_src =  article.find('img',class_='wp-post-image')['data-src']

        #print(img_src)

        img_name = img_src.split('/')[7]

        img_name_id = img_name.split('.')[0]
    except Exception as e: # if the scrapping fails
        img_name_id = None
    print(img_name)
    print()
    csv_writer.writerow([headline,summary,img_name])

csv_file.close()