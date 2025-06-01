import sqlite3
import os
import bcrypt 

# Ruta donde se guardara la base de datos
db_path = './data/users.db'

# Crea la carpeta si no existe
os.makedirs('./data', exist_ok=True)

# Conexion a sqlite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Creacion de tabla
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    ) 
''')

# Usuarios iniciales (LOS DE A1)
init_users = [
    ('Jeferson', '1234'),    # id: 1
    ('Alexander', '123'),    # id: 2
    ('Oscar', '789'),        # id: 3
    ('Graciela', '123456'),  # id: 4 
]

# Elimina todos los usuarios actuales
cursor.execute('DELETE FROM users')

# Insertar usuarios a la base de datos
for username, password in init_users:
    # Tipo de dato byte
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute('''
        INSERT INTO users (username, password) VALUES (?, ?)
    ''', (username, hashed_password.decode('utf-8')))

conn.commit()
conn.close()

print("Base de datos y tabla 'users' creadas correctamente")
print("Usuarios iniciales insertados correctamente")