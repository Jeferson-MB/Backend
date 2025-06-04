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

# Método para consultar si existe algo en la base de datos
def query_db(query, args=(), one=False, commit=False):
    db = get_db()
    cur = db.execute(query, args)
    if commit:
        db.commit()
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# Método para modificar datos existentes en la DB
def modify_db(query, args=()):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    cur.close()
    return cur.lastrowid

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Función init_db que se ejecuta dentro del contexto de la aplicación
def init_db():
    """Inicializa la base de datos dentro del contexto de la aplicación"""
    pass  # La inicialización real se hace en init_sqlite.py

# ===========================
# NUEVA FUNCIÓN PARA LOGIN
# ===========================
def get_user_by_username(username):
    row = query_db("SELECT username, password, name FROM users WHERE username = ?", [username], one=True)
    if row:
        return {'username': row['username'], 'password': row['password'], 'name': row['name']}
    return None