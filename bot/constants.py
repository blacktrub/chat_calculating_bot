import os

FILE_DIR = os.path.abspath(os.path.dirname(__file__))

TOKEN = None
with open(os.path.join(FILE_DIR, 'token'), 'r') as f:
    TOKEN = f.readline().strip()
