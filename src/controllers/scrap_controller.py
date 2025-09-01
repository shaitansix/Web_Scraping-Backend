import pandas as pd

def extract_data(soup): 
  info_book = soup.find('div', class_ = 'product_main')
  title = info_book.find('h1').text
  price = info_book.find('p', class_ = 'price_color').text
  stock = list(info_book.find('p', class_ = 'instock availability').children)[-1].strip()
  rating = info_book.find('p', class_ = 'star-rating').get('class')[-1]
  description = soup.find('div', attrs = {'id': 'product_description'}).find_next_sibling('p').text

  return title, price, stock, rating, description

def format_data(title, price, stock, rating, description): 
  rating_dict = {
    'one': 1, 
    'two': 2, 
    'three': 3, 
    'four': 4, 
    'five': 5
  }
  
  price = float(price[1:])
  stock = int(stock.split(' ')[2][1:])
  rating = rating_dict[rating.lower()]
  
  columns = ['title', 'price(EUR)', 'stock', 'rating', 'description']
  data = pd.DataFrame([[title, price, stock, rating, description]], columns = columns)
  return data

def add_data(df, data): 
  if df is None: 
    return data.copy()
  return pd.concat([df, data])