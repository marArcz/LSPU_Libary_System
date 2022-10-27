import sqlite3

from flask import Flask

app = Flask(__name__)
db_name = "library-system.db"

def init_db():
    db = sqlite3.connect(db_name)  
    print("Database opened successfully")  

    with app.open_resource('database.sql', mode='r') as f:
        db.cursor().executescript(f.read())

    print("Table created successfully")  
    db.close()   

init_db()

