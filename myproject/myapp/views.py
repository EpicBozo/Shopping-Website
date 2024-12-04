from django.shortcuts import render
from django.http import HttpResponse
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from django.shortcuts import redirect
from selenium.common.exceptions import NoSuchElementException #debugging selenium


# Create your views here.

# Selenium

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--disable-dev-shm-usage')  # Optimize memory usage
chrome_options.add_argument('--no-sandbox')  # Linux only
chrome_options.add_argument('--disable-images')  # Disable images
chrome_options.add_argument('--disable-extensions')
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

def index(request):
    return render(request, 'myapp/index.html')

def scrape(request):
    product_id = request.GET.get('search')
    product_list = []
    product_list.append(scrape_ali(product_id))
    product_list.append(scrape_amazon(product_id))
    product_list.append(scrape_ebay(product_id))
    
    return render(request, 'myapp/results.html', {"product_list": product_list, "product_id": product_id, "product_count": len(product_list)})

def link_generation(product_id):
    company_links = {}
    ali_id = product_id.replace(" ", "-")
    amazon_ebay_id = product_id.replace(" ", "+")
    amazon_link = "https://www.amazon.com/s?k=" + ali_id
    ebay_link = "https://www.ebay.com/sch/i.html?_nkw=" + amazon_ebay_id
    ali_link = "https://www.aliexpress.us/w/wholesale-" + amazon_ebay_id + ".html"
    company_links["amazon"] = amazon_link
    company_links["ebay"] = ebay_link
    company_links["ali"] = ali_link

    return company_links

def scrape_amazon(product_id):
    link = link_generation(product_id)
    url = link["amazon"]
    driver.get(url)
    
    page_height = driver.execute_script("return document.body.scrollHeight")

    scroll_increment = 300
    scroll_pause = 0.1

    current_scroll = 0
    products =[]
    
    product_list = []
    return product_list

def scrape_ebay(product_id):
    link = link_generation(product_id)
    url = link["ebay"]
    driver.get(url)
    
    page_height = driver.execute_script("return document.body.scrollHeight")

    scroll_increment = 300
    scroll_pause = 0.1

    current_scroll = 0
    products =[]
    
    product_list = []
    return product_list

def scrape_ali(product_id):
    link = link_generation(product_id)
    url = link["ali"]
    driver.get(url)

     #Gets height of the entire page
    page_height = driver.execute_script("return document.body.scrollHeight")

    scroll_increment = 300
    scroll_pause = 0.1

    current_scroll = 0
    products =[]

    while current_scroll < page_height:
        driver.execute_script(f"window.scrollTo(0, {current_scroll});")
        if driver.find_elements(By.CSS_SELECTOR, '#card-list .list--gallery--C2f2tvm.search-item-card-wrapper-gallery'):
            products= driver.find_elements(By.CSS_SELECTOR, '#card-list .list--gallery--C2f2tvm.search-item-card-wrapper-gallery')
            current_scroll += scroll_increment
            time.sleep(scroll_pause)
        

        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height > page_height:
            page_height = new_height  
        elif current_scroll >= page_height:  
            break
    
    print(len(products))
    print(products)
    # initialize hashmap
    products_list = []

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
                product_images = product_images_elements[0].get_attribute('src') if product_images_elements else None
                products_list.append({"names": product_names, "price": product_price, "images": product_images})

    # Todo, fix the random product_names error
    
    return products_list

# This broke today shi got me tweaking
def sort_price(request):
    if request.method == 'GET':
        sort_type = request.GET.get('sort-by')
        products_list = request.session.get('product_list',[])
        sorted_list = []
        if sort_type == "low-to-high":
            low_high_list = sorted(products_list, key=lambda x: float(x['price'].replace('$', '').replace(',', '')))
            sorted_list = low_high_list
        if sort_type == "high-to-low":
            high_low_list= sorted(products_list, key=lambda x: float(x['price'].replace('$', '').replace(',', '')) ,reverse=True)
            sorted_list = high_low_list
    return render(request,'myapp/results.html',{"product_list": sorted_list, "product_id": request.session.get('product_id')})

def price_range(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    products_list = request.session.get('product_list',[])
    filtered_list = []
    for product in products_list:
        price = float(product['price'].replace('$', '').replace(',', ''))
        if price >= float(min_price) and price <= float(max_price):
            filtered_list.append(product)
    
    return render(request, 'myapp/results.html', {"product_list": filtered_list, "product_id": request.session.get('product_id')})