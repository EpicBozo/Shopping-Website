from django.shortcuts import render
from django.http import HttpResponse
import time
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from django.shortcuts import redirect
from selenium.common.exceptions import NoSuchElementException #debugging selenium
from seleniumwire import webdriver as seleniumwirewebdriver
from .hidden_config import API_KEY


# Create your views here.

# Selenium
proxy = f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001'

def proxy_driver():
    try:
        print("Called proxy driver")
        chrome_options_with_proxy = Options()
        chrome_options_with_proxy.add_experimental_option("detach", True)
        #chrome_options_with_proxy.add_argument('--headless')
        chrome_options_with_proxy.add_argument('--disable-gpu')
        chrome_options_with_proxy.add_argument('--disable-dev-shm-usage')
        chrome_options_with_proxy.add_argument('--no-sandbox')
        chrome_options_with_proxy.add_argument('--disable-images')
        chrome_options_with_proxy.add_argument('--disable-extensions')
        chrome_options_with_proxy.add_argument('--proxy-server=%s' % proxy)
        driver = seleniumwirewebdriver.Chrome(service=service, options=chrome_options_with_proxy)
        print("Proxy driver created successfully")
        return driver
    except Exception as e:
        print(f"Error in proxy_driver: {e}")

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--disable-dev-shm-usage')  # Optimize memory usage
chrome_options.add_argument('--no-sandbox')  # Linux only
chrome_options.add_argument('--disable-images')  # Disable images
chrome_options.add_argument('--disable-extensions')
service = Service()

def index(request):
    try:
        print("Rendering index page")
        return render(request, 'myapp/index.html')
    except Exception as e:
        print(f"Error in index view: {e}")

def get_product_info_view(request):
    try:
        print("Getting product info view")
        product_id = request.GET.get('search')
        
        async def run_async_function():
            return await get_product_info(request)
        
        product_list = asyncio.run(run_async_function())
        print("Product info retrieved successfully")
        return render(request, 'myapp/results.html', {"product_list": product_list, "product_id": product_id, "product_count": len(product_list)})
    except Exception as e:
        print(f"Error in get_product_info_view: {e}")

async def get_product_info(request):
    try:
        print("Getting product info")
        product_id = request.GET.get('search')
        product_list = []
        ali_task = asyncio.create_task(scrape_ali(product_id))
        amazon_task = asyncio.create_task(scrape_amazon(product_id))
        #ebay_task = asyncio.create_task(scrape_ebay(product_id))
        try:
            ali_products, amazon_products = await asyncio.gather(ali_task, amazon_task)
            print("Scraping tasks completed")
        except Exception as e:
            print(f"Error in asyncio.gather: {e}")
            ali_products = []
            amazon_products = []

        product_list = ali_products + amazon_products
        print("Product list combined")
        
        return product_list
    except Exception as e:
        print(f"Error in get_product_info: {e}")

def element_handling(modal, class_name):
    try:
        print(f"Handling element with class name: {class_name}")
        if " " in class_name:
            class_name = class_name.replace(" ", ".")
            element =  modal.find_elements(By.CSS_SELECTOR, f'.{class_name}')
        else:
            element =  modal.find_elements(By.CLASS_NAME, class_name)
        print(f"Element handling completed for class name: {class_name}")
        return element
    except Exception as e:
        print(f"Error in element_handling: {e}")

async def scrape(url, modal_link, product_name, product_price, product_image, product_link, driver):
    try:
        print(f"Scraping URL: {url}")
        driver.get(url)
        
        # Gets height of the entire page
        page_height = driver.execute_script("return document.body.scrollHeight")

        scroll_increment = 300
        scroll_pause = 0.1

        current_scroll = 0
        products = []

        while current_scroll < page_height:
            print(f"Current scroll: {current_scroll}, Page height: {page_height}")
            driver.execute_script(f"window.scrollTo(0, {current_scroll});")
            css_selector = modal_link.replace(" ", ".")
            modal_paramter = f'#card-list .{css_selector}'
            if driver.find_elements(By.CSS_SELECTOR, modal_paramter):
                products = driver.find_elements(By.CSS_SELECTOR, modal_paramter)
                current_scroll += scroll_increment
                await asyncio.sleep(scroll_pause)

            new_height = driver.execute_script("return document.body.scrollHeight")
            
            if new_height > page_height:
                page_height = new_height  
            elif current_scroll >= page_height:  
                break
        
        print(f"Scraping completed for URL: {url}")
        products_list = []

        for modal in products:
            product_names_elements = element_handling(modal, product_name)
            product_price_elements = element_handling(modal, product_price)
            product_images_elements = element_handling(modal, product_image)

            if len(product_names_elements) == len(product_price_elements):
                for i in range(len(product_names_elements)):
                    product_names = product_names_elements[i].text
                    product_prices = product_price_elements[i].text
                    product_images = product_images_elements[0].get_attribute('src') if product_images_elements else None
                    products_list.append({"names": product_names, "price": product_prices, "images": product_images})
        
        driver.quit()
        print(f"Scraping results processed for URL: {url}")
        return products_list
    except Exception as e:
        print(f"Error in scrape: {e}")

def link_generation(product_id):
    try:
        print(f"Generating links for product ID: {product_id}")
        company_links = {}
        ali_id = product_id.replace(" ", "-")
        amazon_ebay_id = product_id.replace(" ", "+")
        amazon_link = "https://www.amazon.com/s?k=" + amazon_ebay_id
        ebay_link = "https://www.ebay.com/sch/i.html?_nkw=" + amazon_ebay_id
        ali_link = "https://www.aliexpress.us/w/wholesale-" + ali_id + ".html"
        company_links["amazon"] = amazon_link
        company_links["ebay"] = ebay_link
        company_links["ali"] = ali_link
        print(f"Links generated for product ID: {product_id}")

        return company_links
    except Exception as e:
        print(f"Error in link_generation: {e}")

async def scrape_amazon(product_id):
    try:
        print("Scraping Amazon")
        driver = proxy_driver()
        link = link_generation(product_id)
        url = link["amazon"]

        product_modal_link = 'puisg-row'
        product_name_link = 'a-size-medium a-color-base a-text-normal'
        product_price_link = 'a-offscreen'
        product_image_link = 's-image'
        product_links_link = ".s-main-slot .s-result-item"
        
        products_list = await scrape(url, product_modal_link, product_name_link, product_price_link, product_image_link, product_links_link, driver)
        print("Amazon scraping completed")
        return products_list
    except Exception as e:
        print(f"Error in scrape_amazon: {e}")

# def scrape_ebay(product_id):
#     link = link_generation(product_id)
#     url = link["ebay"]
#     driver.get(url)
    
#     product_list = []
#     return product_list

async def scrape_ali(product_id):
    try:
        print("Scraping Ali")
        driver = seleniumwirewebdriver.Chrome(service=service, options=chrome_options)
        link = link_generation(product_id)
        url = link["ali"]

        product_modal_link = 'list--gallery--C2f2tvm search-item-card-wrapper-gallery'
        product_names_link = 'multi--titleText--nXeOvyr'
        product_price_link = 'multi--price-sale--U-S0jtj'
        product_image_link= 'images--item--3XZa6xf'
        product_links_link = ".multi-container .cards .search-card-item"
        products_list = await scrape(url, product_modal_link, product_names_link, product_price_link, product_image_link, product_links_link, driver)
        print("Ali scraping completed")

        return products_list
    except Exception as e:
        print(f"Error in scrape_ali: {e}")

def sort_price(request):
    try:
        print("Sorting products by price")
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
        print("Products sorted by price")
        return render(request,'myapp/results.html',{"product_list": sorted_list, "product_id": request.session.get('product_id')})
    except Exception as e:
        print(f"Error in sort_price: {e}")

def price_range(request):
    try:
        print("Filtering products by price range")
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        products_list = request.session.get('product_list',[])
        filtered_list = []
        for product in products_list:
            price = float(product['price'].replace('$', '').replace(',', ''))
            if price >= float(min_price) and price <= float(max_price):
                filtered_list.append(product)
        
        print("Products filtered by price range")
        return render(request, 'myapp/results.html', {"product_list": filtered_list, "product_id": request.session.get('product_id')})
    except Exception as e:
        print(f"Error in price_range: {e}")