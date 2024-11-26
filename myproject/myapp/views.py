from django.shortcuts import render
from django.http import HttpResponse
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

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

   

def results(request):
    text = request.POST.get('search')
    scraper(text)
    return render(request, 'myapp/results.html', {'text': text})



