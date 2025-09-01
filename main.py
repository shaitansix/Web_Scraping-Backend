from fastapi import FastAPI
from src.routes import scrap_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title = 'Scraping API', version = '1.0.0')

origins = [
  'http://localhost:5173/', 
  'http://127.0.0.1:5173/', 
  'http://localhost:5173', 
  'http://127.0.0.1:5173'
]

app.add_middleware(
  CORSMiddleware, 
  allow_origins = origins, 
  allow_credentials = True, 
  allow_methods = ['*'], 
  allow_headers = ['*']
)

app.include_router(scrap_routes.router)