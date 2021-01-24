from dotenv import load_dotenv
load_dotenv()

import os

token = os.getenv('CF_TOKEN')

jsonbin_key = os.getenv('JSONBIN_KEY')
jsonbin_id = os.getenv('JSONBIN_ID')
