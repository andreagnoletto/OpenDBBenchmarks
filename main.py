import os
import time
import mysql.connector
import psycopg
import firebirdsql
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from psycopg import sql

# Load environment variables from .env
load_dotenv()

NUM_CREATE = 1000000
NUM_READ   = 1000000
NUM_UPDATE = 1000000
NUM_DELETE = 1000000

# Functions to perform CRUD operations on each DB

def mysql_crud_operations():
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )
    cursor = conn.cursor()
    # Create the database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('MYSQL_DB')}")

    print(f"Database '{os.getenv('MYSQL_DB')}' checked/created.")
    # Create table
    cursor.execute("CREATE TABLE IF NOT EXISTS test (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")

    # Measure times
    insert_time, read_time, update_time, delete_time = 0, 0, 0, 0

    # Insert operation
    start_time = time.time()
    for i in range(NUM_CREATE):
        cursor.execute("INSERT INTO test (name) VALUES ('Test Name')")
        conn.commit()
    insert_time = time.time() - start_time

    # Read operation
    start_time = time.time()
    for i in range(NUM_READ):
        cursor.execute(f"SELECT * FROM test WHERE id = {i}")
        cursor.fetchall()
    read_time = time.time() - start_time

    # Update operation
    start_time = time.time()
    for i in range(NUM_UPDATE):
        cursor.execute(f"UPDATE test SET name = 'Updated Name' WHERE id = {i}")
        conn.commit()
    update_time = time.time() - start_time

    # Delete i operation
    start_time = time.time()
    for i in range(NUM_DELETE): #delete i
        cursor.execute(f"DELETE FROM test WHERE id = {i}")
        conn.commit()
    delete_time = time.time() - start_time

    conn.close()

    return insert_time, read_time, update_time, delete_time


def create_postgres_db():
    # Conecta ao banco de dados "postgres" para criar outros bancos de dados
    conn = psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname="postgres"  # Banco de dados padrão
    )

    # Habilita o autocommit apenas para a criação do banco
    with conn.cursor() as cursor:
        conn.autocommit = True  # Necessário para criar banco de dados
        db_name = os.getenv("POSTGRES_DB")

        # Verifica se o banco de dados já existe
        cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [db_name])
        if not cursor.fetchone():
            # Se não existe, cria o banco de dados
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"Database {db_name} created.")
        else:
            print(f"Database {db_name} already exists.")

    conn.close()


def postgres_crud_operations():
    create_postgres_db()
    try:
        conn = psycopg.connect(
            host=os.getenv("POSTGRES_HOST"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
        print("Connection successful")
    except Exception as e:
        print(f"An error occurred: {e}")
    conn = psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname="postgres", # default database
        # dbname=os.getenv("POSTGRES_DB"),
    )
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY, name VARCHAR(255))")
    conn.commit()

    # Perform CRUD operations and measure times
    insert_time, read_time, update_time, delete_time = 0, 0, 0, 0

    start_time = time.time()
    for i in range(NUM_CREATE):
        cursor.execute("INSERT INTO test (name) VALUES ('Test Name')")
        conn.commit()
    insert_time = time.time() - start_time

    start_time = time.time()
    for i in range(NUM_READ):
        cursor.execute(f"SELECT * FROM test WHERE id = {i}")
        cursor.fetchall()
    read_time = time.time() - start_time

    start_time = time.time()
    for i in range(NUM_UPDATE):
        cursor.execute(f"UPDATE test SET name = 'Updated Name' WHERE id = {i}")
        conn.commit()
    update_time = time.time() - start_time

    start_time = time.time()
    for i in range(NUM_DELETE):
        cursor.execute(f"DELETE FROM test WHERE id = {i}")
        conn.commit()
    delete_time = time.time() - start_time

    conn.close()

    return insert_time, read_time, update_time, delete_time


def firebird_crud_operations():
    conn = firebirdsql.connect(
        host=os.getenv("FIREBIRD_HOST"),
        database=os.getenv("FIREBIRD_DB"),
        port=int(os.getenv("FIREBIRD_PORT")),
        user=os.getenv("FIREBIRD_USER"),
        password=os.getenv("FIREBIRD_PASSWORD")
    )
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE test (id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY, name VARCHAR(255))")

    # Perform CRUD operations and measure times
    insert_time, read_time, update_time, delete_time = 0, 0, 0, 0

    start_time = time.time()
    for i in range(1000):
        cursor.execute("INSERT INTO test (name) VALUES ('Test Name')")
    conn.commit()
    insert_time = time.time() - start_time

    start_time = time.time()
    cursor.execute("SELECT * FROM test")
    cursor.fetchall()
    read_time = time.time() - start_time

    start_time = time.time()
    cursor.execute("UPDATE test SET name = 'Updated Name' WHERE id = 1")
    conn.commit()
    update_time = time.time() - start_time

    start_time = time.time()
    cursor.execute("DELETE FROM test WHERE id = 1")
    conn.commit()
    delete_time = time.time() - start_time

    conn.close()

    return insert_time, read_time, update_time, delete_time


# Plotting results
def plot_results(results):
    dbs = list(results.keys())
    insert_times = [results[db][0] for db in dbs]
    read_times = [results[db][1] for db in dbs]
    update_times = [results[db][2] for db in dbs]
    delete_times = [results[db][3] for db in dbs]

    plt.figure(figsize=(10, 6))
    plt.plot(dbs, insert_times, label='Insert', marker='o')
    plt.plot(dbs, read_times, label='Read', marker='o')
    plt.plot(dbs, update_times, label='Update', marker='o')
    plt.plot(dbs, delete_times, label='Delete', marker='o')

    plt.title('CRUD Performance Comparison - less is better')
    plt.xlabel('Databases')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    # Run tests and collect results
    db_results = {
        'MariaDB': mysql_crud_operations(),
        'PostgreSQL': postgres_crud_operations(),
        #'Firebird': firebird_crud_operations(),
    }
    plot_results(db_results)

