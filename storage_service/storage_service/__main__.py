"""Root file for the storage service module"""

import logging
from dotenv import load_dotenv

from storage_service.storage_service import StorageService

logging.basicConfig(level=logging.INFO)
load_dotenv()
StorageService()
