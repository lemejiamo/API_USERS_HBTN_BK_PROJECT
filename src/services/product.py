from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from settings import Settings

settings = Settings()


def get_all_products_service():
    pass

def get_product_service(product_id):
    pass

def create_product_service(product_id , data):
    pass

def update_product_service(product_id , data):
    pass

def delete_product_service(product_id):
    pass
