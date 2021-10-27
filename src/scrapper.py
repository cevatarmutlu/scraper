import re
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def isProductPage(url):
    res = requests.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')

    productDetail = soup.find("div", {"id": "productDetail"})

    if not productDetail:
        return False
    return productDetail

def getProductName(page):
    productInfo = page.find("div", {"id": "productInfo"})
    productName = productInfo.h1.text.replace("\n", "").strip()
    return productName


def getOffer(priceDiscountSec):
    offerTag = priceDiscountSec.find("div", {"class": "detay-indirim"})
    offer = 0 if offerTag == None else offerTag.text.strip()
    logger.info(f"Product offer value: {offer}")
    return offer

def getProductPrice(priceDiscountSec):
    productPriceTag = priceDiscountSec.find("span", {"class": "currencyPrice discountedPrice"})
    productPrice = 0 if productPriceTag == None else productPriceTag.text.replace("TL", "").strip()
    logger.info(f"Product price value: {productPrice}")
    return productPrice

def getSalePrice(priceDiscountSec):
    salePriceTag = priceDiscountSec.find("span", {"class": "product-price"})
    salePrice = 0 if salePriceTag == None else salePriceTag.text.strip()
    logger.info(f"Product sale price value: {salePrice}")
    return salePrice

def getProductAvailability(page):
    newSizeVariant = page.find("div", {"class": re.compile("new-size-variant")})
    aTag = newSizeVariant.find_all("a")
    passiveTags = newSizeVariant.find_all("a", {"class": re.compile("passive")})
    aTagSize = len(aTag)
    passiveTagSize = len(passiveTags)
    
    productAvailabilityRaw = (aTagSize - passiveTagSize) * 100 / aTagSize
    productAvailability = f"{str(round(productAvailabilityRaw, 2)).replace('.', ',')}%"

    logger.info(f"Product availability: {productAvailability}")
    return productAvailability

def getProductCode(page):
    productCodeRaw = page.find("div", {"class": "product-feature-content"}).contents[-1]
    if productCodeRaw == "\n":
        productCodeRaw = page.find("div", {"class": "product-feature-content"}).find("div", {"style": "text-align: left;"}).contents[-1]
    # elif productCode.find("Yerli üretim"):
    #     productCode = productCode.split("Yerli üretim")[1]
    productCode = 0 if productCodeRaw == None else productCodeRaw.strip()
    logger.info(f"Product code: {productCode}")
    return productCode

def scrapper(url):
    page = isProductPage(url=url)

    if page != False:
        logger.info("This page is Product Page")
        
        productName = getProductName(page)
        logger.info(f"Product name: {productName}")

        priceDiscountSec = page.find("div", {"class": re.compile("price-discount-sec")})
        if priceDiscountSec != None:
            logger.info(f"In this page included price-discount-sec")

            offer = getOffer(priceDiscountSec)
            productPrice = getProductPrice(priceDiscountSec)
            salePrice = getSalePrice(priceDiscountSec)
        else:
            logger.info("In this page not included price-discount-sec")
            offer = productPrice = salePrice = None
            
        productAvailability = getProductAvailability(page)

        productCode = getProductCode(page)

        return [url, productCode ,productName, productAvailability, offer, productPrice, salePrice]
    else:
        logger.info("This page is not Product Page")
        return None

# if __name__ == '__main__':
#     url = "https://www.markastok.com/le-ville-tac-orgu-sac-asa-hediye-karlar-ulkesi-kralicesi-elsa-kiz-cocuk-elbise-5804646-mavi"
#     print(scrapper(url))