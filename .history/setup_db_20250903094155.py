import mysql.connector
from mysql.connector import errorcode

# Configure your MySQL credentials
config = {
    'user': 'root',
    'password': '',  # Set this if you changed your root password
    'host': 'localhost',
}

# Database and table names
DB_NAME = 'job_portal'

TABLES = {}

# Job Seekers
TABLES['users'] = (
    "CREATE TABLE IF NOT EXISTS users ("
    "  id INT AUTO_INCREMENT PRIMARY KEY,"
    "  name VARCHAR(100) NOT NULL,"
    "  email VARCHAR(100) NOT NULL UNIQUE,"
    "  password VARCHAR(255) NOT NULL,"
    "  role ENUM('job_seeker') DEFAULT 'job_seeker',"
    "  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    ") ENGINE=InnoDB"
)

# Employers
TABLES['employers'] = (
    "CREATE TABLE IF NOT EXISTS employers ("
    "  id INT AUTO_INCREMENT PRIMARY KEY,"
    "  name VARCHAR(100) NOT NULL,"
    "  email VARCHAR(100) NOT NULL UNIQUE,"
    "  password VARCHAR(255) NOT NULL,"
    "  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    ") ENGINE=InnoDB"
)

# Jobs posted by employers
TABLES['jobs'] = (
    "CREATE TABLE IF NOT EXISTS jobs ("
    "  id INT AUTO_INCREMENT PRIMARY KEY,"
    "  company VARCHAR(100) NOT NULL,"
    "  title VARCHAR(100) NOT NULL,"
    "  department VARCHAR(100),"
    "  job_type VARCHAR(50),"
    "  experience VARCHAR(100),"
    "  salary VARCHAR(50),"
    "  location VARCHAR(100),"
    "  description TEXT,"
    "  skills TEXT,"
    "  employer_id INT,"
    "  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
    "  FOREIGN KEY (employer_id) REFERENCES employers(id)"
    ") ENGINE=InnoDB"
)

# Job applications or matches (optional)
TABLES['applications'] = (
    "CREATE TABLE IF NOT EXISTS applications ("
    "  id INT AUTO_INCREMENT PRIMARY KEY,"
    "  user_id INT,"
    "  job_id INT,"
    "  name VARCHAR(255),"
    "  email VARCHAR(255),"
    "  phone VARCHAR(20),"
    "  resume_url TEXT,"
    "  status VARCHAR(50) DEFAULT 'pending',"
    "  applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
    "  FOREIGN KEY (user_id) REFERENCES users(id),"
    "  FOREIGN KEY (job_id) REFERENCES jobs(id)"
    ") ENGINE=InnoDB"
)

TABLES['saved_jobs'] = (
    "CREATE TABLE IF NOT EXISTS saved_jobs ("
    "  id INT AUTO_INCREMENT PRIMARY KEY,"
    "  user_id INT NOT NULL,"
    "  job_id INT NOT NULL,"
    "  saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
    "  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,"
    "  FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)


# Connect to MySQL and create DB + tables
def create_database_and_tables():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Create database if not exists
        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8mb4'")
            print(f"✔️ Database `{DB_NAME}` created or already exists.")
        except mysql.connector.Error as err:
            print(f"❌ Failed to create database: {err}")
            return

        # Use the database
        cnx.database = DB_NAME

        # Create each table
        for table_name, ddl in TABLES.items():
            try:
                cursor.execute(ddl)
                print(f"✅ Table `{table_name}` created successfully.")
            except mysql.connector.Error as err:
                print(f"❌ Failed creating table `{table_name}`: {err}")

        cursor.close()
        cnx.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("❌ Access denied. Check your username or password.")
        else:
            print(err)

if __name__ == '__main__':
    create_database_and_tables()
