import re
from typing import List, Optional, Tuple, Union
import requests
from bs4 import BeautifulSoup
import bs4
import logging

logger = logging.getLogger(__name__)

def isProductPage(url: str) -> Union[bool, bs4.element.Tag]:
    """
        Returns whether this url is product page or not.
        
        Args:
            url(str): URL to check
        
        Returns:
            (False | Tag): If the page is product page returns product detail section(include required values in this project) of product page otherwise returns false.

    """

    assert type(url) == str, "url variable must be str."

    res = requests.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')

    productDetail = soup.find("div", {"id": "productDetail"})

    if not productDetail:
        return False
    return productDetail

def getProductName(productDetail: bs4.element.Tag) -> str:
    """
        Returns product name

        Args:
            productDetail(Tag): Tag that include product name
        
        Returns:
            (str): product name

    """

    assert type(productDetail) == bs4.element.Tag, "productDetail variable must be Tag from bs4.element"

    productInfo = productDetail.find("div", {"id": "productInfo"})
    productName = productInfo.h1.text.replace("\n", "").strip()
    return productName


def getOffer(priceDiscountSec: bs4.element.Tag) -> str:
    """
        returns offer value

        Args:
            priceDiscountSec(Tag): Tag that include offer value
        
        Returns:
            (str): If there is no offer value in parameter tag returns 0(zero) otherwise offer value.
    """

    assert type(priceDiscountSec) == bs4.element.Tag, "priceDiscountSec variable must be Tag from bs4.element"

    offerTag = priceDiscountSec.find("div", {"class": "detay-indirim"})
    offer = "0" if offerTag == None else offerTag.text.strip()
    logger.info(f"Product offer value: {offer}")
    return offer

def getProductPrice(priceDiscountSec: bs4.element.Tag) -> str:
    """
        returns product price

        Args:
            priceDiscountSec(Tag): Tag that include product price
        
        Returns:
            (str): If there is no product price in parameter tag returns 0(zero) otherwise product price.
    """

    assert type(priceDiscountSec) == bs4.element.Tag, "priceDiscountSec variable must be Tag from bs4.element"

    productPriceTag = priceDiscountSec.find("span", {"class": "currencyPrice discountedPrice"})
    productPrice = "0" if productPriceTag == None else productPriceTag.text.replace("TL", "").strip()
    logger.info(f"Product price value: {productPrice}")
    return productPrice

def getSalePrice(priceDiscountSec) -> str:
    """
        returns sale price

        Args:
            priceDiscountSec(Tag): Tag that include sale price
        
        Returns:
            (str): If there is no sale price in parameter tag returns 0(zero) otherwise sale price.
    """

    assert type(priceDiscountSec) == bs4.element.Tag, "priceDiscountSec variable must be Tag from bs4.element"

    salePriceTag = priceDiscountSec.find("span", {"class": "product-price"})
    salePrice = "0" if salePriceTag == None else salePriceTag.text.strip()
    logger.info(f"Product sale price value: {salePrice}")
    return salePrice

def getProductAvailability(productDetail: bs4.element.Tag) -> str:
    """
        Returns product availability.

        For example: if product sizes are S, M, L and there is no L size this function returns 66,66% because there is 2 sizes from three sizes.

        Args:
            productDetail(Tag): Tag that include product availability
        
        Returns:
            (str): returns product availability value
    """

    assert type(productDetail) == bs4.element.Tag, "productDetail variable must be Tag from bs4.element"

    newSizeVariant = productDetail.find("div", {"class": re.compile("new-size-variant")})
    aTag = newSizeVariant.find_all("a")
    passiveTags = newSizeVariant.find_all("a", {"class": re.compile("passive")})
    aTagSize = len(aTag)
    passiveTagSize = len(passiveTags)
    
    productAvailabilityRaw = (aTagSize - passiveTagSize) * 100 / aTagSize
    productAvailability = f"{str(round(productAvailabilityRaw, 2)).replace('.', ',')}%"

    logger.info(f"Product availability: {productAvailability}")
    return productAvailability

def getProductCode(productDetail: bs4.element.Tag) -> str:
    """
        Returns product code.

        Args:
            productDetail(Tag): Tag that include product code.
        
        Returns:
            (str): returns product code
    """

    assert type(productDetail) == bs4.element.Tag, "productDetail variable must be Tag from bs4.element"
    
    productCodeRaw = productDetail.find("div", {"class": "product-feature-content"}).contents[-1]
    if productCodeRaw == "\n":
        productCodeRaw = productDetail.find("div", {"class": "product-feature-content"}).find("div", {"style": "text-align: left;"}).contents[-1]
    productCode = "0" if productCodeRaw == None else productCodeRaw.strip()
    logger.info(f"Product code: {productCode}")
    return productCode

def hasPriceDiscountSec(productDetail: bs4.element.Tag) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
        Checks whether price-discount-sec in the page or not

        Args:
            productDetail(Tag): Tag that include price-discount-sec.
        
        Returns:
            (str): retuns tuple. If the page include price-discount-sec returns (offer, productPrice, salePrice) otherwise (None, None, None)
    """
    priceDiscountSec = productDetail.find("div", {"class": re.compile("price-discount-sec")})

    if priceDiscountSec != None:
            logger.info(f"In this page included price-discount-sec")

            offer = getOffer(priceDiscountSec)
            productPrice = getProductPrice(priceDiscountSec)
            salePrice = getSalePrice(priceDiscountSec)
    else:
        logger.info("In this page not included price-discount-sec")
        offer = productPrice = salePrice = None
    
    return offer, productPrice, salePrice

def scrapper(url: str) -> Optional[List]:
    """
        Returns scraping values

        Args:
            url(str): URL to scrape
        
        Returns:
            (None | list):
    """
    productDetail = isProductPage(url=url)

    if productDetail != False:
        logger.info("This page is Product Page")
        
        productName = getProductName(productDetail)
        logger.info(f"Product name: {productName}")

        offer, productPrice, salePrice = hasPriceDiscountSec(productDetail)

        productAvailability = getProductAvailability(productDetail)

        productCode = getProductCode(productDetail)

        return [url, productCode ,productName, productAvailability, offer, productPrice, salePrice]
    else:
        logger.info("This page is not Product Page")
        return None
