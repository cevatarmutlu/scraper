import requests
from src.scrapper import scrapper
from src.read_excel import get_urls
import re
from src.google_sheet import GoogleSheet
import logging

logging.basicConfig(
        level=logging.DEBUG, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    urls = get_urls("src/resources/URL's.xlsx", "URL", None, 0)
    google = GoogleSheet()
    google.create_sheet("Markastok|Ürün Raporu")


    for url_suffix in urls:
        url_prefix = "https://www.markastok.com"
        url = f"{url_prefix}{url_suffix}"
        logger.info(f"URL: {url}")
        data = scrapper(url)
        google.write_data(data)
        
