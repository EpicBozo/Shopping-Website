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

    while True:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(5) # Loads the whole page

        current_height = driver.execute_script("return document.body.scrollHeight")

        if page_height == current_height:
            break

        page_height = current_height
    
def results(request):
    text = request.POST.get('search')
    scraper(text)
    return render(request, 'myapp/results.html', {'text': text})



