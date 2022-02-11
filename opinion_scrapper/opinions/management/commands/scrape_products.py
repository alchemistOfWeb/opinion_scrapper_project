from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandError, CommandParser
from .product_scraper import lookfor_links, get_driver
from django.conf import settings


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
            msg = "\n___________closing selenium manager!_____________\n"
            self.stdout.write(self.style.WARNING(msg))            

        # print(sitemap[:100])
        

        