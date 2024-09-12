# OpenDBBenchmarks

**OpenDBBenchmarks** is an open-source tool designed to compare the performance of different relational database management systems (RDBMS) in basic CRUD operations (Create, Read, Update, Delete). The goal is to provide clear and measurable benchmarks to help developers and database administrators choose the most efficient solution for their needs.

![Example Image](https://github.com/andreagnoletto/OpenDBBenchmarks/blob/2e92473bfe5cf8c7fabac1080770930d7873f260/Figure_1.png)

## Features:
- Benchmarking for **insert**, **read**, **update**, and **delete** operations.
- Support for multiple databases, including MySQL, MariaDB, PostgreSQL, Firebird, and more.
- Database configuration through `.env` file for ease of use.
- Detailed performance comparison displayed in graphical charts.
- Easily extendable to add support for new databases or custom operations.
- Open-source and free to use for personal and commercial projects.
- Simple and intuitive interface for running benchmark tests and analyzing results.
- Lightweight and fast, with minimal dependencies and resource requirements.

## Getting Started:
1. **Clone the repository**:
   ```bash
   git clone https://github.com/andreagnoletto/OpenDBBenchmarks.git
   cd OpenDBBenchmarks
    ```
2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
    or
   ```bash
   pip install mysql-connector-python psycopg firebirdsql python-dotenv matplotlib
   ```
3. **Configure the environment**:
    - Create a `.env` file in the root directory of the project.
    - Add the following environment variables to the `.env` file:
        ```bash
        DB_HOST=your_database_host
        DB_PORT=your_database_port
        DB_USER=your_database_user
        DB_PASSWORD=your_database_password
        DB_NAME=your_database_name
        isql 'localhost://path/to/firebird.fbd' -user SYSDBA -password masterkey

        ```
    - Replace `your_database_host`, `your_database_port`, `your_database_user`, `your_database_password`, and `your_database_name` with your database credentials.
    - Save the `.env` file.
    - **Note**: If you are using a database other than MySQL, MariaDB, or PostgreSQL, you may need to install additional dependencies. Refer to the documentation of the specific database for more information.
   
4. **Run the benchmark tests**:
    - Run the following command to start the benchmark tests:
        ```bash
        python main.py
        ```
    - The script will run the CRUD operations on the configured database and display the results in a window like example image above.
    ~~- The results will also be saved in a CSV file in the `results` directory.~~
5. **Contribute**:
    - If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on the GitHub repository.
    - Your contributions are welcome and appreciated!
6. **License**:
    - This project is licensed under the MIT License. See the `LICENSE` file for more information.

## Features to be added:
This benchmark tool aims to grow with new features and databases over time. Below are some of the planned improvements:

### 1. Support for Additional Databases
We plan to extend the benchmarking to include the following databases:
- **SQLite**: Lightweight database engine for file-based databases.
- **MariaDB**: High-performance, community-driven fork of MySQL.
- **Oracle Database**: A powerful enterprise-grade RDBMS.
- **Microsoft SQL Server**: A widely used corporate database with advanced tools.
- **MongoDB**: A NoSQL database ideal for large-scale, unstructured data.
- **Cassandra**: A distributed NoSQL database optimized for high availability and large datasets.

### 2. Change of Data Types in CRUD Simulation
In future iterations, we plan to simulate a wider range of CRUD operations using various data types to reflect real-world scenarios. Planned improvements include:
- **Integer and Float** data types for mathematical and financial operations.
- **Date and Time** types for timestamped data, event tracking, etc.
- **Blob and Text fields** for handling large volumes of text and binary data.

### 3. Database-Specific Tuning Parameters
Each database will be tested with multiple tuning configurations to optimize performance. Tuning will involve:
- **Page Size, Cache Settings**: Optimize how data is stored and retrieved.
- **Connection Pooling**: Improve performance for high-concurrency operations.
- **Indexes and Constraints**: Experiment with different indexing strategies to optimize query performance.
- **Memory and Disk I/O**: Optimize resource allocation for better read/write speeds.

### 4. Advanced Benchmarking Metrics
In addition to the basic CRUD operations, we plan to introduce more advanced metrics to evaluate database performance. These metrics include:
- **Query Execution Time**: Measure the time taken to execute complex queries.
- **Concurrency Testing**: Evaluate how databases perform under high-concurrency scenarios.

These features will ensure more comprehensive benchmarks and offer a clearer picture of the performance of each database under different scenarios.

## How You Can Contribute
Feel free to open issues or pull requests if you want to add more databases, propose optimizations, or implement new features!

    
