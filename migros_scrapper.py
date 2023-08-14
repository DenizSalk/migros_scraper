from tkinter import scrolledtext
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import json
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import ThemedTk
import os
import threading
#Ana ekran setup
window = ThemedTk(theme="equilux")
window.config(theme="equilux",bg='#313131')
window.title("İşlem Seçimi")
#Product Info
def run_first_script():
    def scrape_data(file_paths, output_text):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        val = file_paths
        print(val)
        for mcat in val:
            f = open(mcat, "r", encoding="utf-8")
            lines = f.read().splitlines()
            data_list = []
            x = 0
            for url in lines:
                x = x + 1
                output_text.insert(tk.END, "yazılacak ürün: " + url + "\n")
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
                    output_text.insert(tk.END, "kategori bulunamadı\n")
                    categoryf = "Null"
                BrlistToStr = str(categoryf)
                try:
                    name = soup.find('h3', attrs={'class': 'text-color-black'}).get_text()
                except:
                    output_text.insert(tk.END, "isim bulunamadı\n")
                    name = "Null"
                namef = str(name)
                try:
                    brand = soup.find('a', attrs={'class': 'brand-name'}).get_text()
                except:
                    output_text.insert(tk.END, "marka bulunamadı\n")
                    brand = "Null"
                brandf = str(brand)
                try:
                    itemprice = soup.find('span', attrs={'class': 'amount'}).get_text()
                except:
                    output_text.insert(tk.END, "fiyat bulunamadı\n")
                    itemprice = "Null"
                itempricef = str(itemprice)
                data = {
                    'category': BrlistToStr,
                    'name': namef,
                    'brand': brandf,
                    'itemprice': itempricef
                }
                data_list.append(data)
                mcat_basename = os.path.basename(mcat)
                filename = mcat_basename.replace("txt", "json")
                with open(filename, 'w', encoding="utf-8") as f:
                    json.dump(data_list, f, indent=4, ensure_ascii=False)
                output_text.insert(tk.END, "ürün yazıldı \n" + "yazılan toplam ürün: " + str(x) + "\n")
        driver.quit()
    def start_scraping(file_paths):
        if not file_paths:
            output_text.insert(tk.END, "Please select files first.\n")
            return
        threading.Thread(target=scrape_data, args=(file_paths, output_text)).start()
    # Dosya seçim ekranı
    def browse_files(output_text):
        file_paths = filedialog.askopenfilenames(title="Select Value Files", filetypes=[("Text files", "*.txt")])
        output_text.insert(tk.END, "Selected files: {}\n".format(file_paths))
        start_button = ttk.Button(window2, text="Start Scraping", command=lambda: start_scraping(file_paths))
        start_button.pack(pady=10)
    window2 = ThemedTk(theme="arc")
    window2.config(theme="equilux", bg='#313131')
    window2.title("Ürün Bilgisi")
    output_text = tk.Text(window2, wrap=tk.WORD, bg='#313131', fg="#ffffff")
    output_text.pack()
    browse_button = ttk.Button(window2, text="Browse Files", command=lambda: browse_files(output_text))
    browse_button.pack(pady=10)
    window2.mainloop()
#Product List
def run_second_script():
    def scrape_data(urls, is_virtual_market):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        value_parameter = "?sayfa="
        val_end = "&sirala=onerilenler"
        for link in urls:
            link_temp = str(link)
            wait = WebDriverWait(driver, 10)
            nomorepage = False
            if is_virtual_market:
                filename = link_temp.replace("https://www.migros.com.tr/elektronik/", "") + ".txt"
            else:
                filename = link_temp.replace("https://www.migros.com.tr/", "") + ".txt"
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
                            with open(filename, 'a') as f:
                                f.write("https://www.migros.com.tr" + writecurrent + "\n")
                    else:
                        nomorepage = True
                else:
                    break
        driver.quit()
    # Function to handle the "Scrape" button click
    def start_scraping():
        input_urls = url_textbox.get("1.0", "end-1c").splitlines()
        is_virtual_market = virtual_market_var.get() == 1
        scrape_data(input_urls, is_virtual_market)
        result_label.config(text="Scraping complete.")
    # Create the main GUI window
    window3 = ThemedTk(theme="arc")
    window3.config(theme="equilux", bg='#313131')
    window3.title("Ürün Listesi")
    frm = ttk.Frame(window3)
    # Create and place GUI elements
    url_label = ttk.Label(window3, text="Enter URLs (one per line):")
    url_label.pack()
    url_textbox = scrolledtext.ScrolledText(window3, height=10, width=40)
    url_textbox.pack()
    virtual_market_var = tk.IntVar()
    virtual_market_checkbox = ttk.Checkbutton(window3, text="Ekstra", variable=virtual_market_var)
    virtual_market_checkbox.pack()
    scrape_button = ttk.Button(window3, text="Scrape", command=start_scraping)
    scrape_button.pack(pady=100)
    result_label = ttk.Label(window3, text="", wraplength=300, justify="center")
    result_label.pack()
    ttk.Button(frm, text="Close Window", command=window3.destroy).grid(column=1, row=0)
    window3.mainloop()
first_script_button = ttk.Button(window, text="Product Info", command=run_first_script)
first_script_button.pack(padx=100,pady=100)

second_script_button = ttk.Button(window, text="Product List", command=run_second_script)
second_script_button.pack(padx=100,pady=100)

window.mainloop()
