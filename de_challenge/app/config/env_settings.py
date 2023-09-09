import os

if not os.getenv('ENVIRONMENT', False):
    print('sono qui')
    from dotenv import load_dotenv
    load_dotenv('/.env',)

#Database env variables
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

print(DB_HOST, DB_PORT, DB_PASSWORD, DB_NAME, DB_USER)