from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    #MySQL
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST= os.getenv("MYSQL_HOST")
    MYSQL_PORT= os.getenv("MYSQL_PORT")
    MYSQL_DB= os.getenv("MYSQL_DB")

    DATABASE_URL = (f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}")

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

settings = Settings()

