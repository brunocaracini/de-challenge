import os
import socket

if not os.getenv('ENVIRONMENT', False):
    print('sono qui')
    # Use socket.gethostbyname to resolve the hostname to an IP address
    db_host = socket.gethostbyname("db")

    # You can print the resolved IP address for debugging purposes
    print(f"Resolved DB host IP: {db_host}")
    from dotenv import load_dotenv
    load_dotenv('/.env',)

#Database env variables
DB_HOST = socket.gethostbyname("db")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

print(DB_HOST, DB_PORT, DB_PASSWORD, DB_NAME, DB_USER)