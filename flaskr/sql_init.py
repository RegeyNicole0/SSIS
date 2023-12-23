from config import DB_HOST, DB_PASSWORD,DB_USERNAME, DB_NAME, DB_PORT
import mysql.connector



mydb = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USERNAME,
    password=DB_PASSWORD,
    port=DB_PORT
)
mycursor = mydb.cursor()

def create_db():
    mycursor.execute(f"""
        CREATE DATABASE IF NOT EXISTS {DB_NAME};
        USE {DB_NAME};

        CREATE TABLE colleges (
            college_code        VARCHAR(20) NOT NULL,
            college_name 		VARCHAR(100) NOT NULL,
            PRIMARY KEY(college_code),
            UNIQUE(college_name)
        );
                     
    """
    )