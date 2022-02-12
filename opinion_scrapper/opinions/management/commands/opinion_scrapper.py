import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from opinions.models import Opinion, Product


AVAILABLE_TITLES = {
        'достоинства': 'advantages',
        'недостатки': 'disadvantages',
        'комментарий': 'content'
    }


def count_stars(bs_stars_node):
    stars_num = 0

    for star in bs_stars_node:
        if star['data-state'] == 'selected':
            stars_num += 1

    return stars_num


def scrape_opinions_of_product(product_url, driver):
    opinions_url = product_url+'opinion' if product_url[-1] == '/' else product_url+'opinion'

    print('REQUEST URL: ', opinions_url)
    driver.get(opinions_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    bs_opinion_blocks = soup.find(
        class_='ow-opinions')

    if not bs_opinion_blocks:
        return None

    bs_opinion_blocks = bs_opinion_blocks.find_all(class_='ow-opinion')
    opinion_list = []

    for bs_opinion_node in bs_opinion_blocks:
        opinion = dict()

        bs_stars = bs_opinion_node.find(class_='star-rating__stars')
        opinion['stars_num'] = count_stars(bs_stars)

        bs_texts = bs_opinion_node.find(class_='ow-opinion__texts')

        for av_title in AVAILABLE_TITLES.values():
            print(av_title)
            opinion[av_title] = ''
        
        if bs_texts:
            bs_texts = bs_texts.find_all(class_='ow-opinion__text')

            for bs_text in bs_texts:                
                text_title = bs_text.find(
                    class_='ow-opinion__text-title').string.lower()

                if text_title in AVAILABLE_TITLES.keys():
                    text_content = bs_text.find(
                        class_='ow-opinion__text-desc').get_text()
                    opinion[AVAILABLE_TITLES[text_title]] = text_content

        using_duration = bs_opinion_node.find(
            class_='ow-opinion__info-desc').string
        opinion['using_duration'] = using_duration

        opinion['source'] = bs_opinion_node.find(
            class_='ow-opinion__site').string
        opinion['author_name'] = bs_opinion_node.find(
            class_='profile-info__name').string

        opinion['comments_num'] = '0'
        bs_comments_num = bs_opinion_node.find(
            class_='ow-opinion__comments')

        if bs_comments_num:
            searched = re.search(r'\((\d+)\)', bs_comments_num.a.span.string)
            opinion['comments_num'] = searched.group(1) if searched else 0


        opinion_list.append(opinion)

    return opinion_list


def scrape_opinions(driver, limit=None):
    if limit:
        products = Product.objects.all()[:limit]
    else:
        products = Product.objects.all()
    
    for product in products:
        print(product.url)
        opinion_list = scrape_opinions_of_product(product.url, driver)

        if not opinion_list:
            continue

        print('opinionlist: ', opinion_list)

        for opinion in opinion_list:
            Opinion.objects.update_or_create(defaults=opinion, 
                                            author_name=opinion['author_name'], 
                                            content=opinion['content'], 
                                            product=product)
        
