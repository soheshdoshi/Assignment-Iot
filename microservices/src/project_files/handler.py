from mangum import Mangum
from main import app  # here we have app in main.py

handler = Mangum(app)
