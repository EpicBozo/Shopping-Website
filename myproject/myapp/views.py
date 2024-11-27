from django.shortcuts import render
from django.http import HttpResponse
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Create your views here.

#Selenium

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

def index(request):
    return render(request, 'myapp/index.html')

def scraper(product_id):
    product_id = product_id.replace(" ", "-")
    url = "https://www.aliexpress.us/w/wholesale-" + product_id + ".html"
    driver.get(url)

    #Gets height of the entire page
    page_height = driver.execute_script("return document.body.scrollHeight")

    scroll_increment = 200
    scroll_pause = 0.5

    current_scroll = 0

    while current_scroll < page_height:
        driver.execute_script(f"window.scrollTo(0, {current_scroll});")
        current_scroll += scroll_increment
        time.sleep(scroll_pause)

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height > page_height:
            page_height = new_height  
        elif current_scroll >= page_height:  
            break

    product_names = driver.find_elements(By.CLASS_NAME, 'multi--title--G7dOCj3')

    time.sleep(1)

    for product in product_names:
        print(product.text)

    
def results(request):
    text = request.POST.get('search')
    scraper(text)
    return render(request, 'myapp/results.html', {'text': text})



