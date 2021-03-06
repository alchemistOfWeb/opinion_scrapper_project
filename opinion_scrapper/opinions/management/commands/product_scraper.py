from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from urllib.parse import urljoin, urlencode, urlparse, urlunparse, parse_qsl
from opinions.models import Product

def add_params_to_url(url, params_dict):
    url_parts = list(urlparse(url))
    query = dict(parse_qsl(url_parts[4]))
    query.update(params_dict)
    url_parts[4] = urlencode(query)

    return urlunparse(url_parts)


def search_products_node(soup):
    return soup.find(class_="catalog-products")


def search_subcategory_node(soup):
    return soup.find(class_="subcategory")


def get_subcategory_links(soup_node, host):
    subcategory_items = soup_node.find_all(class_="subcategory__item")
    subcategory_links = []

    for subcategory_item in subcategory_items:
        if "subcategory__item_with-childs" in subcategory_item['class']:
            child_items = subcategory_item.find_all(
                class_="subcategory__childs-list-item")
            # replace find_all on select method with ".subcategory__childs-list-item a"
            for child_item in child_items[1:]:
                full_url = urljoin(host, child_item.a['href'])
                subcategory_links.append(full_url)
        else:
            full_url = urljoin(host, subcategory_item['href'])
            subcategory_links.append(full_url)

    return subcategory_links


def get_product_links(soup_node, host):
    product_cards = soup_node.find_all(class_="catalog-product__name")
    product_links = []

    for card in product_cards:
        full_url = urljoin(host, card['href'])
        product_title = card.get_text()
        set_product_into_db({'title': product_title, 'url': full_url})
        product_links.append(full_url)

    return product_links


def set_products_into_db(product_list:list):
    queryset = Product.objects

    for product in product_list:
        defaults = {'title': product['title'], 'url': product['url']}
        queryset.update_or_create(url=product['url'], defaults=defaults)


def set_product_into_db(product:dict):
    defaults = {'title': product['title'], 'url': product['url']}
    Product.objects.update_or_create(url=product['url'], defaults=defaults)


def lookfor_links(driver, current_url, host, sitemap_list=[], page_number=None, last_page_number=None):
    if page_number:
        request_url = add_params_to_url(current_url, {"p": page_number})
    else:
        request_url = current_url # 1: host + uri

    print('\nREQUEST URL: ', request_url)
    
    driver.get(request_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    bs_products_node = search_products_node(soup)
    bs_subcategory_node = search_subcategory_node(soup)
    thereis_products = bool(bs_products_node)
    thereis_subcategory = bool(bs_subcategory_node)

    assert (thereis_products or thereis_subcategory), "There is neither products nor subcategories"

    if thereis_subcategory:
        subcategory_links = get_subcategory_links(bs_subcategory_node, host)
        for link in subcategory_links:
            sitemap_list = lookfor_links(driver, link, host, sitemap_list)
    elif thereis_products:
        if not page_number:
            page_number = 1

        if not last_page_number:
            last_page_selector_str = '.pagination-widget__pages>li:last-child'
            last_page_selector = soup.select(last_page_selector_str)

            if last_page_selector:
                last_page_number = int(last_page_selector[0]['data-page-number'])            
            else:
                last_page_number = 1


        found_products_list = get_product_links(bs_products_node, host)
        print(found_products_list)
        sitemap_list.extend(found_products_list)

        if page_number < last_page_number:
            page_number += 1
            sitemap_list = lookfor_links(driver, current_url, host, sitemap_list,
                          page_number, last_page_number)

    return sitemap_list
