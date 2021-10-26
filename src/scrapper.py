import re
import requests
from bs4 import BeautifulSoup

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
    offer = priceDiscountSec.find("div", {"class": "detay-indirim"})
    return 0 if offer == None else offer.text.strip()

def getProductPrice(priceDiscountSec):
    productPrice = priceDiscountSec.find("span", {"class": "currencyPrice discountedPrice"})
    return 0 if productPrice == None else productPrice.text.replace("TL", "").strip()

def getSalePrice(priceDiscountSec):
    salePrice = priceDiscountSec.find("span", {"class": "product-price"})
    return 0 if salePrice == None else salePrice.text.strip()

def getProductAvailability(page):
    newSizeVariant = page.find("div", {"class": re.compile("new-size-variant")})
    aTag = newSizeVariant.find_all("a")
    passiveTags = newSizeVariant.find_all("a", {"class": re.compile("passive")})
    aTagSize = len(aTag)
    passiveTagSize = len(passiveTags)
    
    productAvailability = (aTagSize - passiveTagSize) * 100 / aTagSize
    return f"{productAvailability}%"

def scrapper(url):
    page = isProductPage(url=url)

    if page != False:
        productName = getProductName(page)

        priceDiscountSec = page.find("div", {"class": re.compile("price-discount-sec")})
        if priceDiscountSec != None:
            offer = getOffer(priceDiscountSec)
            productPrice = getProductPrice(priceDiscountSec)
            salePrice = getSalePrice(priceDiscountSec)
        else:
            offer = productPrice = salePrice = None
            
        productAvailability = getProductAvailability(page)

        return [url, productName, productAvailability, offer, productPrice, salePrice]
    else:
        return None