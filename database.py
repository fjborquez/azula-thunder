import mysql.connector
from mysql.connector import errorcode

from enums.observations import Observations
from enums.status import Status
from secrets_handler import get_secret

def create_transition(detail, new_status: Status, is_active: bool, observation: Observations):
    query = ("INSERT INTO product_status_transitions (inventory_id, product_status_id, is_active, created_at, updated_at,"
             " observations) VALUES (%s, %s, %s, NOW(), NOW(), %s)")
    data = (detail['id'], new_status.value, is_active, observation.value)
    mydb, cursor = connect()
    cursor.execute(query, data)
    mydb.commit()
    cursor.close()
    mydb.close()

def change_active_transition(detail, is_active: bool):
    query = "UPDATE product_status_transitions SET is_active = %s WHERE inventory_id = %s"
    data = (is_active, detail['id'])
    mydb, cursor = connect()
    cursor.execute(query, data)
    mydb.commit()
    cursor.close()
    mydb.close()

def connect():
    host = get_secret("db_host")
    user = get_secret("db_user")
    password = get_secret("db_password")
    database = get_secret("db_name")

    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    return mydb, mydb.cursor()