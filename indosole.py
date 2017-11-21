from urllib.request import urlopen as uReg
import urllib.request
from bs4 import BeautifulSoup as soup
import time
import pandas as pd

# *****INDOSOLE PRODUCTS**********

def collectPageProducts(page_soup):
    page_title = page_soup.findAll("header", {"class": "section-header"})

    if len(page_title) == 0:
        page_title = page_soup.findAll("h1")

    pageName = page_title[0].text.strip()

    # find all products
    containers = page_soup.findAll("div", {"grid-product__wrapper"})
    products = containers[:-1]
    productDictList = []
    for product in products:
        image_url = product.div.a.img["src"]

        product_url = "https://indosole.com" + product.div.a["href"]

        product_name = product.div.a.img["alt"]

        container_Price = product.findAll("span", {"class": "grid-product__price"})
        reg_price = container_Price[0].text.strip()

        reqDes = urllib.request.Request(product_url, headers={"User-Agent": "Mozilla/5.0"})
        htmlDes = urllib.request.urlopen(reqDes).read()
        page_soupDes = soup(htmlDes, "html.parser")
        desContainer = page_soupDes.findAll("div", {"product-single__description rte"})
        product_description = desContainer[0].text.strip()

        time.sleep(0.5)

        productDict = {
            "imageSrc": image_url,
            "url": product_url,
            "name": product_name,
            "price": reg_price,
            "description": product_description,
            "category": pageName
        }
        productDictList.append(productDict)
    return productDictList

def main():
    # ********WEB PAGES************
    webPages = ["https://indosole.com/collections/women-essntls",
                "https://indosole.com/collections/womens-sandals",
                "https://indosole.com/collections/womens-shoes",
                "https://indosole.com/collections/men-essntls",
                "https://indosole.com/collections/mens-sandals",
                "https://indosole.com/collections/mens-shoes"]

    # *******WEB PAGES HTML PARSERS*****

    allProducts = []
    for webPage in webPages:
        req = urllib.request.Request(webPage, headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(req).read()
        page_soup = soup(html, "html.parser")

        theseProducts = collectPageProducts(page_soup)
        allProducts.extend(theseProducts)

    productsDataFrame = pd.DataFrame(allProducts)
    productsDataFrame.to_csv("indosole.py")
