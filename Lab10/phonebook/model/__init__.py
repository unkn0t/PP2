import config
import psycopg2
import sys

try:
    CONFIG = config.load(sys.argv[1])
except:
    raise Exception("Expected config filename as first argument.")

class ModelManager:
    def __init__(self) -> None:
        self.db = psycopg2.connect(**CONFIG)
        
    def __del__(self) -> None:
        self.db.close()

