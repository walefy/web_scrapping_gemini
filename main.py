import warnings

warnings.filterwarnings('ignore')

import os
import json
from selenium import webdriver
from bs4 import BeautifulSoup, Tag, ResultSet
from typing import List
from dotenv import load_dotenv
from time import sleep

from src.model import ArticleItem
from src.service import TTSService
from src.service import AIService
from src.data import agents

load_dotenv()

BASE_URL = os.environ['BASE_URL']


def validate_tag(element: object) -> Tag:
    if not isinstance(element, Tag):
        raise ValueError("element is\'nt a tag!")
    return element


def get_summary(article: ArticleItem, ai_service: AIService, max_tries: int, try_count = 0):
    if try_count >= max_tries:
        raise ValueError('Gemini service error!')

    try:
        article.summary = ai_service.ask(article.model_dump_json())
    except ValueError:
        print('error, retrying in 20s...')
        sleep(20)
        get_summary(article, ai_service, max_tries, try_count=try_count+1)


def main():
    ai_service = AIService(agent=agents.SUMMARIZE_ARTICLE_AGENT)
    tts_service = TTSService()

    os.environ['MOZ_HEADLESS'] = '1'
    driver = webdriver.Firefox()
    driver.get(BASE_URL)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    articles_list = validate_tag(soup.find('ol'))

    article_items_search: ResultSet[Tag] = articles_list.find_all('li')
    article_items_list_filtered = article_items_search[1:]

    article_items: List[ArticleItem] = []
    article_items_with_error: List[ArticleItem] = []

    for item in article_items_list_filtered:
        aside_item = validate_tag(item.findChild())
        div_item = validate_tag(aside_item.findChild())
        link_item = validate_tag(div_item.findChild())

        link_url = BASE_URL + str(link_item.get('href'))
        title = link_item.text

        article_item = ArticleItem(title=title, link=link_url)
        print(article_item, end='\n\n')

        driver.get(article_item.link)

        article_item_soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles_inside_item: ResultSet[Tag] = article_item_soup.find_all('article')
        articles_inside_item_strs = [validate_tag(a.find('div', { 'class': 'markdown-body' })).text for a in articles_inside_item]

        article_item.content = articles_inside_item_strs[0]
        article_item.comments = articles_inside_item_strs[1:]

        try:
            get_summary(article_item, ai_service, 3)
            audio_path = tts_service.generate_audio(title=article_item.title,
                                                    text=article_item.summary.summary) # type: ignore
            article_item.audio_path = audio_path
            article_items.append(article_item)
        except ValueError:
            article_items_with_error.append(article_item)
            print('error, skipping...')

    with open('output/report.json', 'w', encoding='utf-8') as file:
        data = [a.model_dump() for a in article_items]
        file.write(json.dumps(data, indent=2, ensure_ascii=False))

    print(f'{'=' * 10} items with error: {len(article_items_with_error)} {'=' * 10}')
    for item in article_items_with_error:
        print(item)

    driver.close()

if __name__ == '__main__':
    main()
