import sqlite3
from sqlite3 import Error

class QueriesSQLite:
    @staticmethod
    def create_connection(db_file):
        """Create a database connection to the SQLite database specified by db_file."""
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(e)
        return conn

    @staticmethod
    def execute_query(connection, query, data=None):
        """Execute a single query."""
        try:
            cursor = connection.cursor()
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    @staticmethod
    def execute_read_query(connection, query):
        """Execute a read query and return results."""
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def create_tables(connection):
        """Create tables if they do not exist."""
        create_usuarios_table = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            password TEXT NOT NULL,
            tipo TEXT NOT NULL
        );
        """
        create_productos_table = """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL
        );
        """
        create_ventas_table = """
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            cantidad INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (producto_id) REFERENCES productos (id)
        );
        """
        create_proveedores_table = """
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL UNIQUE
        );
        """
        create_clientes_table = """
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL UNIQUE
        );
        """
        create_estado_compra_table = """
        CREATE TABLE IF NOT EXISTS estado_compra (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estado TEXT NOT NULL
        );
        """
        create_estado_venta_table = """
        CREATE TABLE IF NOT EXISTS estado_venta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estado TEXT NOT NULL
        );
        """
        create_categorias_table = """
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        );
        """
        create_compras_table = """
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            proveedor_id INTEGER,
            cantidad INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (producto_id) REFERENCES productos (id),
            FOREIGN KEY (proveedor_id) REFERENCES proveedores (id)
        );
        """
        create_pagos_table = """
        CREATE TABLE IF NOT EXISTS pagos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            cantidad REAL NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        );
        """
        
        QueriesSQLite.execute_query(connection, create_usuarios_table)
        QueriesSQLite.execute_query(connection, create_productos_table)
        QueriesSQLite.execute_query(connection, create_ventas_table)
        QueriesSQLite.execute_query(connection, create_proveedores_table)
        QueriesSQLite.execute_query(connection, create_clientes_table)
        QueriesSQLite.execute_query(connection, create_estado_compra_table)
        QueriesSQLite.execute_query(connection, create_estado_venta_table)
        QueriesSQLite.execute_query(connection, create_categorias_table)
        QueriesSQLite.execute_query(connection, create_compras_table)
        QueriesSQLite.execute_query(connection, create_pagos_table)

    @staticmethod
    def get_all_ventas():
        """Get all ventas from the database."""
        query = "SELECT * FROM ventas"
        connection = QueriesSQLite.create_connection("pdvDB.sqlite")
        if connection is not None:
            return QueriesSQLite.execute_read_query(connection, query)
        else:
            print("Error! Cannot create the database connection.")

# Example usage:
# if __name__ == "__main__":
#     conn = QueriesSQLite.create_connection("pdvDB.sqlite")
#     QueriesSQLite.create_tables(conn)
