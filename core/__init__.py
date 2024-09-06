from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import event
from sqlalchemy.engine import Engine
from pymysql import install_as_MySQLdb
import os

# Install pymysql as MySQLdb
install_as_MySQLdb()

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Load configuration from config.py
    app.config.from_object('core.config.Config')
    
    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # SQLite foreign key enforcement (only if using SQLite)
    @event.listens_for(Engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):
        if isinstance(dbapi_connection, SQLite3Connection):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()
    
    @app.route('/')
    def index():
        # Example query
        sql_docs = db.session.execute("SELECT * FROM my_table").fetchall()  # Replace 'my_table' with your table name
        # resp = make_response("Setting a cookie")
        # resp.set_cookie('my_cookie', 'cookie_value')
        return jsonify({
            "sql_docs": [dict(row) for row in sql_docs],
        })
        # resp
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)





# from flask import Flask, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from sqlalchemy import event
# from sqlalchemy.engine import Engine
# from sqlite3 import Connection as SQLite3Connection
# from pymongo import MongoClient
# import os
# import pymysql
# pymysql.install_as_MySQLdb()

# app = Flask(__name__)

# # SQLite configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./store.sqlite3'
# app.config['SQLALCHEMY_ECHO'] = False
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# app.test_client()

# # MongoDB configuration
# mongo_uri = os.getenv('MONGO_URI', "mongodb://127.0.0.1:27017/assi")
# mongo_client = MongoClient(mongo_uri)
# mongo_db = mongo_client.myDatabaseName  # Replace with your actual MongoDB database name

# # SQLite foreign key enforcement
# @event.listens_for(Engine, "connect")
# def _set_sqlite_pragma(dbapi_connection, connection_record):
#     if isinstance(dbapi_connection, SQLite3Connection):
#         cursor = dbapi_connection.cursor()
#         cursor.execute("PRAGMA foreign_keys=ON;")
#         cursor.close()

# @app.route('/')
# def index():
#     # Example MongoDB query
#     mongo_collection = mongo_db.myCollectionName  # Replace with your actual collection name
#     mongo_docs = list(mongo_collection.find())  # Get all documents from the collection

#     # Example SQLite query
#     sql_docs = db.session.execute("SELECT * FROM my_table").fetchall()  # Replace 'my_table' with your table name

#     return jsonify({
#         "mongo_docs": mongo_docs,
#         "sql_docs": [dict(row) for row in sql_docs]
#     })

# if __name__ == '__main__':
#     app.run(debug=True)


