import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
import datetime

# specify the url of the website
url = 'https://www.theverge.com/'

# send a GET request to the url
response = requests.get(url)

# parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# get all the articles from the homepage
articles = soup.find_all('article')

# set up the CSV file with the current date
today = datetime.datetime.now().strftime('%d%m%Y')
csv_file = f'{today}_verge.csv'
csv_header = ['id', 'URL', 'headline', 'author', 'date']

# set up the SQLite database
conn = sqlite3.connect('theverge.db')
c = conn.cursor()

# create the table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS articles
             (id INTEGER PRIMARY KEY,
              URL TEXT,
              headline TEXT,
              author TEXT,
              date TEXT)''')

# iterate over the articles and extract the data
for i, article in enumerate(articles):
    # extract the headline and URL
    headline = article.h2.a.text.strip()
    url = article.h2.a['href']

    # extract the author and date
    metadata = article.find('div', {'class': 'c-byline'}).text.strip().split('•')
    author = metadata[0].strip()
    date = metadata[1].strip()

    # insert the data into the CSV file
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([i+1, url, headline, author, date])

    # insert the data into the SQLite database
    c.execute('''INSERT OR IGNORE INTO articles
                 (id, URL, headline, author, date)
                 VALUES (?, ?, ?, ?, ?)''', (i+1, url, headline, author, date))

# commit the changes to the database
conn.commit()

# close the database connection
conn.close()
