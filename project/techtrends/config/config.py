import os
import logging
from dotenv import load_dotenv

load_dotenv()


class Config:
    port = os.getenv('PORT')
    host = os.getenv('HOST')
    secret_key = os.getenv('SECRET_KEY')

    def logger(self):
        formatter = logging.Formatter(
            '%(asctime)s, %(message)s', datefmt="%m/%d/%Y %I:%M:%S %p %Z")
        handler = logging.FileHandler(filename='app.log')
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        logger = logging.getLogger('status')
        logger.addHandler(handler)        
