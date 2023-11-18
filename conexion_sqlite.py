import sqlite3

class ConexionSQLite:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT,
                producto TEXT,
                precio REAL
            )
        ''')
        self.conn.commit()

    def insert_producto(self, codigo, producto, precio):
        self.cur.execute('''
            INSERT INTO productos (codigo, producto, precio)
            VALUES (?, ?, ?)
        ''', (codigo, producto, precio))
        self.conn.commit()

    def get_productos(self):
        self.cur.execute('SELECT * FROM productos')
        return self.cur.fetchall()

    def update_producto(self, id, codigo, producto, precio):
        self.cur.execute('''
            UPDATE productos
            SET codigo = ?, producto = ?, precio = ?
            WHERE id = ?
        ''', (codigo, producto, precio, id))
        self.conn.commit()

    def delete_producto(self, id):
        self.cur.execute('DELETE FROM productos WHERE id = ?', (id,))
        self.conn.commit()

    def get_producto_by_id(self, id):
        self.cur.execute('SELECT * FROM productos WHERE id = ?', (id,))
        return self.cur.fetchone()
    def __del__(self):
        self.conn.close()
        
# accion = SQLiteHandler("lista_de_precios.db")
# accion.insert_producto('123', 'Té', '10.99')
# print(accion.get_productos())
