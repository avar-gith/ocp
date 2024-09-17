# file: adan/views/storage.py

from datetime import timedelta

# Token alapú adat tárolás
data_store = {}
token_expiry_time = timedelta(hours=1)  # Token érvényességi ideje
