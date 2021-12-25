import requests
from bs4 import BeautifulSoup as BS


def scrapper_news_article_for_habr(headers_, list_of_tags):
    response = requests.get(url='https://habr.com/ru/all', headers=headers_)
    response.raise_for_status()
    text = response.text
    soup = BS(text, features='html.parser')
    articles = soup.find_all('article')
    for article in articles:
        tags = article.find_all('a', class_='tm-article-snippet__hubs-item-link')
        tags = set(tag.find('span').text for tag in tags)
        date = article.find('time')
        title = article.find('a', class_='tm-article-snippet__title-link')
        span_title = title.find('span').text
        link = 'https://habr.com' + title['href']
        article_response = requests.get(url=link, headers=headers_)
        response.raise_for_status()
        article_text = article_response.text
        article_soup = BS(article_text, features='html.parser')
        article_content_text = article_soup.find_all('p')
        article_content_text = [paragraph.text for paragraph in article_content_text]
        all_article_text = ' '.join(article_content_text)
        for word in list_of_tags:
            if word in all_article_text or set(list_of_tags) & tags:
                print(date['title'].split(',')[0], '-', span_title, '-', link)
                print('_ _ _ _ _')
