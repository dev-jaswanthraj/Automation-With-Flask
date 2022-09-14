import os

class Config(object):
    
    SECRET_KEY = os.environ.get('SECRETE_KEY') or 'kfjdn98758tn84uW#$09u4'

    #* Database Configuration 
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:0987@localhost/FlaskDB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #* Static File Configuration
    UPLOAD_FOLDER = 'C:/Users/HP/Desktop/TCS Python Project/FlaskProject/app/Static/Other'
    MAX_CONTENT_PATH = 1024