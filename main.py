import os
import time
import mysql.connector
import psycopg
import firebirdsql
from dotenv import load_dotenv
import matplotlib.pyplot as plt

# Load environment variables from .env
load_dotenv()

NUM_CREATE = 10000
NUM_READ   = 10000
NUM_UPDATE = 10000
NUM_DELETE = 10000


def perform_crud_operations(db_type, conn, cursor):
    """Generic function to perform CRUD operations and measure execution times."""
    insert_time, read_time, update_time, delete_time = 0, 0, 0, 0

    # Insert operation
    start_time = time.time()
    for _ in range(NUM_CREATE):
        cursor.execute("INSERT INTO test (name) VALUES ('Test Name')")
    conn.commit()
    insert_time = time.time() - start_time

    # Read operation
    start_time = time.time()
    for i in range(1, NUM_READ + 1):
        cursor.execute(f"SELECT * FROM test WHERE id = {i}")
        cursor.fetchall()
    read_time = time.time() - start_time

    # Update operation
    start_time = time.time()
    for i in range(1, NUM_UPDATE + 1):
        cursor.execute(f"UPDATE test SET name = 'Updated Name' WHERE id = {i}")
    conn.commit()
    update_time = time.time() - start_time

    # Delete operation
    start_time = time.time()
    for i in range(1, NUM_DELETE + 1):
        cursor.execute(f"DELETE FROM test WHERE id = {i}")
    conn.commit()
    delete_time = time.time() - start_time

    return insert_time, read_time, update_time, delete_time


def mysql_crud_operations():
    """Perform CRUD operations on MySQL."""
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS test (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")

    results = perform_crud_operations("MySQL", conn, cursor)
    conn.close()
    return results


def postgres_crud_operations():
    """Perform CRUD operations on PostgreSQL."""
    conn = psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB")
    )
    with conn.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY, name VARCHAR(255))")
        results = perform_crud_operations("PostgreSQL", conn, cursor)
    conn.close()
    return results


def firebird_crud_operations():
    """Perform CRUD operations on Firebird."""
    conn = firebirdsql.connect(
        host=os.getenv("FIREBIRD_HOST"),
        database=os.getenv("FIREBIRD_DB"),
        user=os.getenv("FIREBIRD_USER"),
        password=os.getenv("FIREBIRD_PASSWORD")
    )
    with conn.cursor() as cursor:
        # Verificar se a tabela já existe no Firebird
        cursor.execute("SELECT COUNT(*) FROM rdb$relations WHERE rdb$relation_name = 'TEST'")
        table_exists = cursor.fetchone()[0]

        if table_exists == 0:
            # Criar a tabela se ela não existir
            cursor.execute("CREATE TABLE test (id INT PRIMARY KEY, name VARCHAR(255))")
            conn.commit()

        # Realizar as operações CRUD
        results = perform_crud_operations("Firebird", conn, cursor)

    conn.close()
    return results



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

    plt.title(f'CRUD Performance Comparison - less is better (n={NUM_CREATE})')
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
