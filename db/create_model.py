import mysql.connector
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml'))

ddbb_host = config['DDBB'].get('HOST')
ddbb_user = config['DDBB'].get('USER')
ddbb_name = config['DDBB'].get('DATABASE')
ddbb_pass = config['DDBB'].get('PASS')

def connect_to_ddbb():
    connection = mysql.connector.connect(host=ddbb_host, user=ddbb_user, password=ddbb_pass, database=ddbb_name)
    return connection

def create_ddbb_data():
    connection = None
    try:
        print("Connecting to database...")
        connection = connect_to_ddbb()
        cursor = connection.cursor()
        print("Creating table/s...")
        cursor.execute('''CREATE TABLE IF NOT EXISTS project (
                            project_id INT NOT NULL,
                            start_date INT NOT NULL,
                            proposal_manager TEXT DEFAULT NULL,
                            data_management_system TEXT DEFAULT NULL,
                            metadata_path TEXT DEFAULT NULL,
                            PRIMARY KEY(project_id));''')
        connection.commit()
        print('... tables properly created :)')
    except Exception as e:
        print(f'... Problem creating tables!: {e}')
    finally:
        if connection:
            connection.close()

create_ddbb_data()
