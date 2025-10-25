from fastapi import APIRouter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
from src.controllers import scrap_controller

router = APIRouter(prefix = '/scrap', tags = ['scrap'])

@router.get('/')
async def start(url: str): 
  try: 
    options = webdriver.ChromeOptions()

    # Configuraciones esenciales para Docker
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=9222')
    
    # Solucionar el error del user-data-dir
    options.add_argument('--user-data-dir=/tmp/chrome-profile')
    
    # Otros argumentos recomendados
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-software-rasterizer')

    driver = webdriver.Chrome(options = options)

    driver.get(url)
    images = WebDriverWait(driver, 10).until(
      EC.presence_of_all_elements_located((By.XPATH, '//div[@class="image_container"]'))
    )
    links = [image.find_element(By.TAG_NAME, 'a') for image in images]

    df = None
    for link in links: 
      link.click()

      html = driver.page_source
      soup = bs(html, 'html.parser')
      title, price, stock, rating, description = scrap_controller.extract_data(soup)
      
      data = scrap_controller.format_data(title, price, stock, rating, description)
      df = scrap_controller.add_data(df, data)
      driver.back()
    driver.quit()

    df.reset_index(drop = True, inplace = True)
    return {
      'status': 'success', 
      'data': df.to_dict(orient = 'records'), 
      'statusText': 'The scraping was successfully completed.'
    }
  except Exception as exc: 
    print(exc)
    return {
      'status': 'error', 
      'data': None, 
      'statusText': 'The scraping failed.'
    }