import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

def count_stars(bs_stars_node):
    stars_num = 0

    for star in bs_stars_node:
        if star['data-state'] == 'selected':
            stars_num += 1

    return stars_num


def scrape_opinions_of_product(product_url, driver):
    opinions_url = urljoin(product_url, '/opinion/')

    driver.get(opinions_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    bs_opinion_blocks = soup.find(class_='ow-opinions').find_all(class_='ow-opinion')
    opinion_list = []

    for bs_opinion_node in bs_opinion_blocks:
        opinion = dict()
        
        bs_stars = bs_opinion_node.find(class_='star-rating__stars')
        opinion['stars_num'] = count_stars(bs_stars)

        bs_texts = bs_opinion_node.find(class_='ow-opinion__texts').find_all(class_='ow-opinion__text')

        for bs_text in bs_texts:
            available_titles = {
                'достоинства': 'advantages',
                'недостатки': 'disadvantages',
                'комментарий': 'comment_text'
            }
            text_title = bs_text.find(class_='ow-opinion__text-title').string.lower()

            if text_title in available_titles.keys():
                text_content = bs_text.find(class_='ow-opinion__text-desc').get_text()
                opinion[available_titles[text_title]] = text_content
        
        using_duration = bs_opinion_node.find(class_='ow-opinion__info-desc').string
        opinion['using_duration'] = using_duration

        opinion['source'] = bs_opinion_node.find(class_='ow-opinion__site').string
        opinion['author_name'] = bs_opinion_node.find(class_='profile-info__name').string

        comments_num_str = bs_opinion_node.find(class_='ow-opinion__comments').a.span.string
        searched = re.search(r'\((\d+)\)', comments_num_str)
        opinion['comments_num'] = searched.group(1) if searched else 0

        opinion_list.append(opinion)
    
    return opinion_list
