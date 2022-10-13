from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from settings import Settings

settings = Settings()


def get_all_companies_service():
    pass

def get_company_service(company_id):
    pass

def create_company_service(company_id , data):
    # usar repostiry que conecta con firebase
    pass

def update_company_service(company_id , data):
    pass

def delete_company_service(company_id):
    pass
