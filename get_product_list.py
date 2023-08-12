import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
val = ["https://www.migros.com.tr/oyuncak-c-9e",
       "https://www.migros.com.tr/kitap-dergi-gazete-c-a5"
       ]
value_parameter = "?sayfa="
val_end = "&sirala=onerilenler"
for link in val:
    link_temp = str(link)
    wait = WebDriverWait(driver, 10)
    nomorepage = False
    filename = link_temp.replace("https://www.migros.com.tr/","").replace("?sayfa=", "") + ".txt"
    print(filename)
    print(link_temp)
    for x in range(1, 100):
        if not nomorepage:
            val_final = link_temp + value_parameter + str(x) + val_end
            driver.get(val_final)
            wait.until(EC.url_to_be(val_final))
            time.sleep(5)
            page_source = driver.page_source
            time.sleep(2)
            soup = BeautifulSoup(page_source, 'html.parser')
            soupcheck = str(soup)
            if "bulamadık" not in soupcheck:
                for link in soup.find_all('a', attrs={'class': 'product-name'}):
                    writecurrent = str(link['href'])
                    print(writecurrent)
                    with open(filename, 'a') as f:
                        f.write("https://www.migros.com.tr" + writecurrent + "\n")
            else:
                nomorepage = True
        else:
            break