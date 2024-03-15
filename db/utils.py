import mysql.connector
import configparser
import os
import datetime

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml'))

ddbb_host = config['DDBB'].get('HOST')
ddbb_user = config['DDBB'].get('USER')
ddbb_name = config['DDBB'].get('DATABASE')
ddbb_pass = config['DDBB'].get('PASS')

def connect_to_ddbb():
    connection = mysql.connector.connect(host=ddbb_host, user=ddbb_user, password=ddbb_pass, database=ddbb_name)
    return connection

def check_today_projects():
    today = datetime.datetime.now().strftime('%Y%m%d')
    connection = None
    try:
        connection = connect_to_ddbb()
        cursor = connection.cursor()
        cursor.execute(f'SELECT count(*) FROM project WHERE CAST(project_id AS CHAR) LIKE "{today}%"')
        today_projects = cursor.fetchone()[0]
    except Exception as e:
        print(f'... Problem querying the database: {e}')
    finally:
        if connection:
            connection.close()

    return today_projects

def create_new_project(new_project):
    connection = None
    try:
        connection = connect_to_ddbb()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO project VALUES (%s, %s, %s, %s, %s)', new_project)
        connection.commit()
        print(f'... project created with id {new_project[0]}')
    except Exception as e:
        print(f'... project could not be created because of: {e}')
    finally:
        if connection:
            connection.close()

def update_project(project_id, attribute_name, value):
    connection = None
    try:
        connection = connect_to_ddbb()
        cursor = connection.cursor()
        cursor.execute('UPDATE project SET %s = %s WHERE project_id = %s' % (attribute_name, value, project_id))
        connection.commit()
        print(f'... updated project with id {project_id}')
    except Exception as e:
        print(f'... project could not be updated because of: {e}')
    finally:
        if connection:
            connection.close()

def check_if_project_exists(project_id):
    connection = None
    try:
        connection = connect_to_ddbb()
        cursor = connection.cursor()
        cursor.execute(f'SELECT count(*) FROM project WHERE project_id = %s' % project_id)
        total = cursor.fetchone()[0]
        if total > 0:
            return True
        else:
            return False
    except Exception as e:
        print(f'... could not check projects with id {project_id} because of: {e}')
    finally:
        if connection:
            connection.close()

def delete_project(project_id):
    connection = None
    try:
        connection = connect_to_ddbb()
        cursor = connection.cursor()
        if check_if_project_exists(project_id):
            cursor.execute('DELETE FROM project WHERE project_id = %s' % project_id)
            connection.commit()
            print(f'... deleted project with id {project_id}')
        else:
            print(f'... there is no project with id {project_id}')
    except Exception as e:
        print(f'... project could not be deleted because of: {e}')
    finally:
        if connection:
            connection.close()
