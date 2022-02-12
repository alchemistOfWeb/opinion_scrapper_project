from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandError, CommandParser
from .scrape_products import get_driver
from .opinion_scrapper import scrape_opinions
from django.conf import settings


class Command(BaseCommand):
    help = "launch process of scraping opinions from dns-shop"

    def add_arguments(self, parser: CommandParser) -> None:
        return super().add_arguments(parser)
    
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.stdout.write(self.style.SUCCESS('Start parsing of opinions!'))

        try:
            driver = get_driver(settings.GECKODRIVER_PATH) # perform the function
            parse_limit = 100
            scrape_opinions(driver, parse_limit)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('Scrapping was interrupted!'))
        except Exception as ex:
            self.stdout.write(self.style.ERROR(ex.message))            
        finally:
            driver.close()
            driver.quit()
            msg = "Closing selenium manager!"
            self.stdout.write(self.style.WARNING(msg))
