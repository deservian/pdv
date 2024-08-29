from queries import QueriesSQLite

def main():
    # Conecta a la base de datos
    connection = QueriesSQLite.create_connection("pdvDB.sqlite")

    # Crea las tablas
    QueriesSQLite.create_tables(connection)

    # Inserta un usuario administrador (opcional, puedes hacerlo manualmente)
    # QueriesSQLite.insert_admin_user(connection)

    print("Database and tables created successfully.")

if __name__ == "__main__":
    main()
