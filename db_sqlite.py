import sqlite3
from flask import g
from config import Config

DATABASE = Config.SQLITE_DB

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

# Metodo para consultar si existe algo en la base de datos
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return(rv[0] if rv else None) if one else rv

# Método para modificar datos existentes en la DB
def modify_db(query, args=()):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    cur.close()

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()