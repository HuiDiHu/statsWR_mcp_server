import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Api_Config:
    BASE_URL = os.getenv('STATSWR_API_BASE_URL')
    DEFAULT_TIMEOUT = int(os.getenv('DEFAULT_TIMEOUT'))

    DEFAULT_HEADERS = {
        "User-Agent": "StatsWR-MCP-Server/1.0",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

api_config = Api_Config()
