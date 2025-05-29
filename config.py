import os

class Config:
    UPLOAD_FOLDER = './static/uploads'
    DATA_FOLDER = './data'
    DATABASE_FILE = os.path.join(DATA_FOLDER, 'database.json') # ./data/database.json