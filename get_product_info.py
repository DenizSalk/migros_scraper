import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import json
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
val = [ "kirtasiye-c-11420",
        "kitap-dergi-gazete-c-a5",
        "oyuncak-c-9e"
       ]
for mcat in val:
    mcat_final = mcat + ".txt"
    f = open(mcat_final, "r" , encoding="utf-8")
    lines = f.read().splitlines()
    data_list = []
    x = 0
    for url in lines:
        x = x + 1
        print("yazılacak ürün: "+ url)
        wait = WebDriverWait(driver, 10)
        driver.get(url)
        time.sleep(2)
        page_source = driver.page_source
        categoryf = []
        soup = BeautifulSoup(page_source, 'html.parser', from_encoding='utf-8')
        try:
            for brcrum in soup.find_all('a', attrs={'class': 'breadcrumbs__link'}):
                categoryf.append(brcrum.get_text())
        except:
            print("kategori bulunamadı")
            categoryf = "Null"
        BrlistToStr = str(categoryf)
        try:
            name = soup.find('h3', attrs={'class': 'text-color-black'}).get_text()
        except:
            print("isim bulunamadı")
            name = "Null"
        namef = str(name)
        try:
            brand = soup.find('a', attrs={'class': 'brand-name'}).get_text()
        except:
            print("marka bulunamadı")
            brand = "Null"
        brandf = str(brand)
        try:
            itemprice = soup.find('span', attrs={'class': 'amount'}).get_text()
        except:
            print("fiyat bulunamadı")
            itemprice = "Null"
        itempricef = str(itemprice)
        data = {
                'category': BrlistToStr,
                'name': namef,
                'brand': brandf,
                'itemprice': itempricef
        }
        data_list.append(data)
        filename = mcat_final.replace("txt","json")
        with open(filename , 'w', encoding="utf-8") as f:
            json.dump(data_list, f, indent=4, ensure_ascii=False)
        print("ürün yazıldı \n" + "yazılan toplam ürün: "+ str(x))
