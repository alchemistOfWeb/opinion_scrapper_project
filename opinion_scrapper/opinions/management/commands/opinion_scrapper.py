def scrape_opinions_of_product(product_url, driver, soup):
    opinion_blocks = soup.find_all(class_='.opinion-block')
    opinion_list = []

    for opinion_block in opinion_blocks:
        opinion = dict()
        opinion['text'] = opinion_block.find('.opinion__text').string
        opinion['advantages'] = opinion_block.find('.opinion__adv').string
        opinion['disadvantages'] = opinion_block.find('.opinion__disadv').string
        opinion['using_duration'] = opinion_block.find('.opinion__using-duration').string
        opinion['source'] = opinion_block.find('.opinion__source').string
        opinion['author_name'] = opinion_block.find('.opinion__author').string
        opinion['stars_num'] = opinion_block.find('.opinion__rating').string
        opinion['comments_num'] = opinion_block.find('.opinion__comments-num').string

        opinion_list.append(opinion)
    
    return opinion_list
