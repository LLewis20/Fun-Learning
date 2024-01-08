import datetime
import requests
from bs4 import BeautifulSoup

def get_articles(limit=None, month: int = datetime.datetime.now().month, year: int = datetime.datetime.now().year):
    month = str(month).zfill(2)
    URL = f'https://www.nwmissouri.edu/media/news/{year}/{month}/'

    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('li')
    total_articles = 0

    for article in articles:
        # if the limit is reached, break out of the loop
        if limit is not None and total_articles >= limit:
            break

        title_div = article.find('div', class_='news-text')
        image_div = article.find('div', class_='news-image')

        # getting the title and link from each article
        if title_div and title_div.find('a'):
            title_tag = title_div.find('a')
            title = title_tag.get_text(strip=True)
            link = f"https://www.nwmissouri.edu/media/news/{year}/{month}/" + title_tag['href']

            image_url = None
            if image_div and image_div.find('img') and 'src' in image_div.find('img').attrs:
                image_url = f"https://www.nwmissouri.edu/media/news/{year}/{month}/" + image_div.find('img')['src']

            # getting dates from each article
            get_date = requests.get(link)
            soup = BeautifulSoup(get_date.content, 'html.parser')
            date_elements = soup.find_all('p', class_='date')
            date_wrote = date_elements[0].get_text(strip=True) if date_elements else 'Date not available'
            author = date_elements[1].get_text(strip=True) if len(date_elements) > 1 else 'Northwest Missouri State University Media Center'
            
            
            # getting a description from each article
            description_elements = soup.find_all('p')
            description = description_elements[3].get_text(strip=True) + ' ' + description_elements[4].get_text(strip=True)
            
            total_articles += 1

            yield {
                'title': title,
                'link': link,
                'image_url': image_url,
                'date': date_wrote,
                'author': author,
                'description': description
            }