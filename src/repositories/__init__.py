from settings import Settings
from utils.connect_realtimedatabase import init_firebase_db

settings = Settings

db, db_app = init_firebase_db(db_url=settings.FIREBASE_URL_ONE)
