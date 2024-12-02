from django.shortcuts import render
from django.http import HttpResponse
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from django.shortcuts import redirect
from selenium.common.exceptions import NoSuchElementException #debugging selenium


# Create your views here.

# Selenium

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

def index(request):
    return render(request, 'myapp/index.html')

def scraper(request):
    product_id = request.GET.get('search')
    request.session['product_id'] = product_id
    url_tag = product_id.replace(" ", "-")
    url = "https://www.aliexpress.us/w/wholesale-" + url_tag + ".html"
    driver.get(url)

    #Gets height of the entire page
    page_height = driver.execute_script("return document.body.scrollHeight")

    scroll_increment = 200
    scroll_pause = 0.1

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
    
    
    products = driver.find_elements(By.CSS_SELECTOR, '#card-list .list--gallery--C2f2tvm.search-item-card-wrapper-gallery')

    # initialize hashmap
    products_list = []
    request.session['product_list'] = products_list

    # Todo add images and hyperlinks
    
    for modal in products:
        
        product_names_elements = modal.find_elements(By.CLASS_NAME, 'multi--titleText--nXeOvyr')
        product_price_elements = modal.find_elements(By.CLASS_NAME, 'multi--price-sale--U-S0jtj')
        product_images_elements = modal.find_elements(By.CLASS_NAME, 'images--item--3XZa6xf')
        product_links_elements = modal.find_elements(By.CSS_SELECTOR, ".multi-container .cards .search-card-item")
            
        if len(product_names_elements) == len(product_price_elements):
            for i in range(len(product_names_elements)):
                product_names = product_names_elements[i].text
                product_price = product_price_elements[i].text
                products_list.append({"names": product_names, "price": product_price})

        
        if len(product_images_elements) == 0:
            break
        else: 
            product_images = product_images_elements[0].get_attribute('src')
        products_list.append({"images": product_images})

    # Todo, fix the random product_names error
    
    return render(request, 'myapp/results.html', {"product_list": products_list, "product_id": product_id,"product_images": product_images,"search_found": len(product_names)})

def sort_price(request):
    if request.method == 'GET':
        sort_type = request.GET.get('sort-by')
        products_list = request.session.get('product_list',[])
        if sort_type == "low-to-high":
            low_high_list = sorted(products_list, key=lambda x: float(x['price'].replace('$', '').replace(',', '')))
            sorted_list = low_high_list
        if sort_type == "high-to-low":
            high_low_list= sorted(products_list, key=lambda x: float(x['price'].replace('$', '').replace(',', '')) ,reverse=True)
            sorted_list = high_low_list
    return render(request,'myapp/results.html',{"product_list": sorted_list, "product_id": request.session.get('product_id'), "search_found": len(sorted_list)})