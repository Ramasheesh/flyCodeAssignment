# config.py

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Rama%40123@127.0.0.1:3306/mydatabase'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # For MySQL or PostgreSQL, replace with your URI
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@host/database'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@host/database'
    
    # For MongoDB
    # MONGO_URI = 'mongodb://localhost:27017/myDatabase'
