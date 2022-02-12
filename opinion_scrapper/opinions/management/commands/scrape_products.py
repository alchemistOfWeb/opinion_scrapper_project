from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandError, CommandParser
from .product_scraper import lookfor_links
from django.conf import settings
from selenium import webdriver


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


class Command(BaseCommand):
    help = "launch scraping products from dns-shop"

    def add_arguments(self, parser: CommandParser) -> None:
        return super().add_arguments(parser)
    
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.stdout.write(self.style.SUCCESS('Hello!'))
        host = "https://www.dns-shop.ru" # rename to site_root
        root_url = "https://www.dns-shop.ru/catalog" # rename to full_url or replace on uri

        try:
            driver = get_driver(settings.GECKODRIVER_PATH) # perform the function
            sitemap = lookfor_links(driver, root_url, host) # add driver parameter
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('Scrapping was interrupted!'))
        except Exception as ex:
            self.stdout.write(self.style.ERROR(ex))
        finally:
            driver.close()
            driver.quit()
            msg = "closing selenium manager!"
            self.stdout.write(self.style.WARNING(msg))            

        # print(sitemap[:100])
        