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
  options = webdriver.ChromeOptions()
  options.add_argument('-headless')

  driver = webdriver.Chrome(options = options)
  try: 
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