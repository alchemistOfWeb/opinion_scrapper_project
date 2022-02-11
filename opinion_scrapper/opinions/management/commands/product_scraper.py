from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urllib.parse import urljoin, urlencode, urlparse, urlunparse, parse_qsl

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

    # print(subcategory_links)
    return subcategory_links


def get_product_links(soup_node, host):
    product_cards = soup_node.find_all(class_="catalog-product__name")
    product_links = []

    for card in product_cards:
        full_url = urljoin(host, card['href'])
        product_links.append(full_url)

    # print(product_links)
    return product_links


class SeleniumManager:
    __instance = None

    def __init__(self) -> None:
        options = webdriver.FirefoxOptions()
        options.headless = True        
        USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0" # todo: move it into special options file

        options.set_preference('general.useragent.override', USER_AGENT)
        self.driver = webdriver.Firefox(
            "D:\projects\django_projects\opinions_parser\geckodriver-v0.30.0-win64",
            options=options
        )
        # self.driver.set_window_size(1920, 1080)

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = SeleniumManager()
        return cls.__instance

    def get_source(self, url):
        self.driver.get(url)
        return self.driver.page_source

    def __del__(self):
        if getattr(self, 'driver', False):
            self.driver.close()
            self.driver.quit()

        print("\n___________closing selenium manager!_____________\n")


# def get_data_with_selenium(url):
#     options...
#     try:
#         driver = webdriver.Firefox(...)
#         driver.get(request_url)
#         html = driver.page_source
#     except Exception as ex:
#         print(ex)
#     finally:
#         driver.close()
#         driver.quit()


def lookfor_links(driver, current_url, host, sitemap_list=[], page_number=None, last_page_number=None):
    if page_number:
        request_url = add_params_to_url(current_url, {"p": page_number})
    else:
        request_url = current_url

    print('\nREQUEST URL: ', request_url)
    
    driver.get(request_url)
    html = driver.page_source
    # html = SeleniumManager.get_instance().get_source(request_url)
    soup = BeautifulSoup(html, 'lxml')

    products_node = search_products_node(soup)
    subcategory_node = search_subcategory_node(soup)
    thereis_products = bool(products_node)
    thereis_subcategory = bool(subcategory_node)

    assert (thereis_products or thereis_subcategory), "There is neither products nor subcategories"

    if thereis_subcategory:
        subcategory_links = get_subcategory_links(subcategory_node, host)
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


        found_products_list = get_product_links(products_node, host)
        print(found_products_list)
        sitemap_list.extend(found_products_list)

        if page_number < last_page_number:
            page_number += 1
            sitemap_list = lookfor_links(driver, current_url, host, sitemap_list,
                          page_number, last_page_number)

    return sitemap_list


def get_driver(driver_path):
    options = webdriver.FirefoxOptions()
    options.headless = True        
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0" 
    # todo: move it^ into special options file
    options.set_preference('general.useragent.override', USER_AGENT)
    driver = webdriver.Firefox(
        driver_path,
        options=options
    )

    return driver


if __name__ == '__main__':
    host = "https://www.dns-shop.ru" # rename to site_root
    root_url = "https://www.dns-shop.ru/catalog" # rename to full_url or replace on uri

    try:
        driver = get_driver() # perform the function
        sitemap = lookfor_links(driver, root_url, host) # add driver parameter
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
        print("\n___________closing selenium manager!_____________\n")

    print(sitemap[:100])
