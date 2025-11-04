from collections import namedtuple

import mysql.connector
from mysql.connector import errorcode

from enums.observations import ObservationsEnum
from enums.status import StatusEnum
from secrets_handler import get_secret

def create_transition(detail, new_status: StatusEnum, is_active: bool, observation: ObservationsEnum):
    query = ("INSERT INTO product_status_transitions (inventory_id, product_status_id, is_active, created_at, updated_at,"
             " observations) VALUES (%s, %s, %s, NOW(), NOW(), %s)")

    observation_value = ""

    if type(observation) is str:
        observation_value = observation
    else:
        observation_value = observation.value

    data = (detail['id'], new_status.value, is_active, observation_value)
    mydb, cursor = connect()
    cursor.execute(query, data)
    mydb.commit()
    cursor.close()
    mydb.close()

def change_active_transition(detail, is_active: bool):
    query = "UPDATE product_status_transitions SET is_active = %s, updated_at = NOW() WHERE inventory_id = %s"
    data = (is_active, detail['id'])
    mydb, cursor = connect()
    cursor.execute(query, data)
    mydb.commit()
    cursor.close()
    mydb.close()

def get_current_status(detail):
    query = ("SELECT ps.* "
             "FROM product_status_transitions pst "
             "INNER JOIN product_status ps ON pst.product_status_id = ps.id "
             "WHERE inventory_id = %s AND is_active = 1 LIMIT 1")
    data = (detail['id'],)
    mydb, cursor = connect(dictionary=True)
    cursor.execute(query, data)
    result = cursor.fetchone()
    cursor.close()
    mydb.close()
    return result

def connect(dictionary=False):
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
    return mydb, mydb.cursor(dictionary=dictionary)