import requests
from src.scrapper import scrapper
from src.read_excel import get_urls
import re
from src.google_sheet import GoogleSheet

if __name__ == '__main__':
    urls = get_urls("src/resources/URL's.xlsx", "URL", None, 0)
    google = GoogleSheet()
    google.create_sheet("Markastok|Ürün Raporu")


    for url in urls:
        base_url = "https://www.markastok.com"
        data = scrapper(f"{base_url}{url}")
        print(f"Data: {data}")
        google.write_data(data)
        
