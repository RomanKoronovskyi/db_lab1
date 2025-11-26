import pyodbc
import time
from pymongo import MongoClient
import numpy as np
from datetime import datetime, timedelta
import random

MONGO_URL = "mongodb://localhost:27017/"
MONGO_DB_NAME = "project_management_db"
MONGO_COLLECTION = "timelogs"

SQL_DRIVER = '{ODBC Driver 17 for SQL Server}'
SQL_SERVER = 'DESKTOP-DOSF0HG\\SQLEXPRESS'
SQL_DATABASE = 'management_system_db'

NUM_RECORDS = 100000
TARGET_PROJECT_ID = 50

NUM_TASKS = 500
NUM_USERS = 100
NUM_PROJECTS = 50
NUM_CLIENTS = 10

def get_sql_connection():
    conn_str = (
        f'DRIVER={SQL_DRIVER};'
        f'SERVER={SQL_SERVER};'
        f'DATABASE={SQL_DATABASE};'
        f'Trusted_Connection=yes;'
    )
    return pyodbc.connect(conn_str)

def get_mongo_collection():
    client = MongoClient(MONGO_URL)
    db = client[MONGO_DB_NAME]
    return db[MONGO_COLLECTION]

def setup_sql_master_data(conn):
    cursor = conn.cursor()
    print("\n--- SQL Master Data Setup ---")
    try:
        cursor.execute("DELETE FROM dbo.TimeLogs")
        cursor.execute("DELETE FROM dbo.ClientContacts")
        cursor.execute("DELETE FROM dbo.Tasks")
        cursor.execute("DELETE FROM dbo.Projects")
        cursor.execute("DELETE FROM dbo.Clients")
        cursor.execute("DELETE FROM dbo.Users")
        cursor.execute("DELETE FROM dbo.TaskStatuses")
        cursor.execute("DELETE FROM dbo.TaskPriorities")
        conn.commit()
    except Exception as e:
        print(f"Could not clear some tables: {e}")

    try:
        cursor.execute("SET IDENTITY_INSERT dbo.TaskStatuses ON;")
        cursor.executemany("INSERT INTO dbo.TaskStatuses (ID, status_name) VALUES (?, ?);",
                           [(1, 'Open'), (2, 'In Progress')])
        cursor.execute("SET IDENTITY_INSERT dbo.TaskStatuses OFF;")
        cursor.execute("SET IDENTITY_INSERT dbo.TaskPriorities ON;")
        cursor.executemany("INSERT INTO dbo.TaskPriorities (ID, priority_name) VALUES (?, ?);",
                           [(1, 'High'), (2, 'Medium')])
        cursor.execute("SET IDENTITY_INSERT dbo.TaskPriorities OFF;")
        print("Inserted TaskStatuses and TaskPriorities.")
    except Exception as e:
        print(f"Error during STATUSES/PRIORITIES setup: {e}")
        conn.rollback()
        return

    try:
        user_data = []
        for i in range(1, NUM_USERS + 1):
            user_data.append((
                i,
                f'User {i}',
                'Test_Last',
                f'test_{i}@example.com',
                1
            ))
        cursor.execute("SET IDENTITY_INSERT dbo.Users ON;")
        cursor.executemany("INSERT INTO dbo.Users (ID, first_name, last_name, email, role_id) VALUES (?, ?, ?, ?, ?);",
                           user_data)
        cursor.execute("SET IDENTITY_INSERT dbo.Users OFF;")
        print(f"Inserted {NUM_USERS} records into Users.")
    except Exception as e:
        print(f"Error during USERS setup: {e}")
        conn.rollback()
        return

    try:
        client_data = [(i, f'Client {i}') for i in range(1, NUM_CLIENTS + 1)]
        cursor.execute("SET IDENTITY_INSERT dbo.Clients ON;")
        cursor.executemany("INSERT INTO dbo.Clients (ID, client_name) VALUES (?, ?);", client_data)
        cursor.execute("SET IDENTITY_INSERT dbo.Clients OFF;")
        print(f"Inserted {NUM_CLIENTS} records into Clients.")
    except Exception as e:
        print(f"Error during CLIENTS setup: {e}")
        conn.rollback()
        return

    try:
        project_data = []
        for i in range(1, NUM_PROJECTS + 1):
            project_data.append((
                i,
                f'Project {i}',
                (i % NUM_CLIENTS) + 1,
                (i % NUM_USERS) + 1,
                1,
                1
            ))
        cursor.execute("SET IDENTITY_INSERT dbo.Projects ON;")
        cursor.executemany(
            "INSERT INTO dbo.Projects (ID, project_name, client_id, manager_id, status_id, team_id) VALUES (?, ?, ?, ?, ?, ?);",
            project_data)
        cursor.execute("SET IDENTITY_INSERT dbo.Projects OFF;")
        print(f"Inserted {NUM_PROJECTS} records into Projects.")
    except Exception as e:
        print(f"Error during PROJECTS setup: {e}")
        conn.rollback()
        return

    try:
        task_data = []
        for i in range(1, NUM_TASKS + 1):
            task_data.append((
                i,
                (i % NUM_PROJECTS) + 1,
                (i % NUM_USERS) + 1,
                1,
                1,
                (i % NUM_USERS) + 1,
            ))
        cursor.execute("SET IDENTITY_INSERT dbo.Tasks ON;")
        cursor.executemany(
            "INSERT INTO dbo.Tasks (ID, project_id, assigned_to_user_id, status_id, priority_id, updated_by_user_id) VALUES (?, ?, ?, ?, ?, ?);",
            task_data)
        cursor.execute("SET IDENTITY_INSERT dbo.Tasks OFF;")
        print(f"Inserted {NUM_TASKS} records into Tasks.")
    except Exception as e:
        print(f"Error during TASKS setup: {e}")
        conn.rollback()
        return
    conn.commit()
    print("Master data prepared successfully and committed.")

def test_sql_insert(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dbo.TimeLogs")
    conn.commit()

    start_time = time.time()

    data_to_insert = []
    for i in range(NUM_RECORDS):
        data_to_insert.append((
            (i % NUM_TASKS) + 1,
            (i % NUM_USERS) + 1,
            random.randint(5, 60),
        ))

    query = """
    INSERT INTO dbo.TimeLogs (task_id, user_id, duration_minutes)
    VALUES (?, ?, ?);
    """
    cursor.executemany(query, data_to_insert)
    conn.commit()

    end_time = time.time()
    print(f"SQL Insert Time ({NUM_RECORDS} records): {end_time - start_time} seconds")

def test_mongo_insert(mongo_collection):
    mongo_collection.delete_many({})
    start_time = time.time()

    timelogs = []
    for i in range(NUM_RECORDS):
        timelogs.append({
            "task_id": (i % NUM_TASKS) + 1,
            "user_id": (i % NUM_USERS) + 1,
            "duration_minutes": random.randint(5, 60),
            "logged_at": datetime.now() - timedelta(minutes=i),
            "project_id": (i % NUM_PROJECTS) + 1,
        })

    mongo_collection.insert_many(timelogs, ordered=False)
    end_time = time.time()
    print(f"MongoDB Insert Time ({NUM_RECORDS} records): {end_time - start_time} seconds")

def test_sql_query(conn):
    cursor = conn.cursor()

    query = f"""
    SELECT SUM(L.duration_minutes) 
    FROM dbo.TimeLogs L
    JOIN dbo.Tasks T ON L.task_id = T.ID
    WHERE T.project_id = ?;
    """

    start_time = time.time()
    for _ in range(100):
        cursor.execute(query, (TARGET_PROJECT_ID,))
        cursor.fetchone()
    end_time = time.time()

    print(f"SQL Aggregation Query Time: {(end_time - start_time) / 100} seconds (average)")

def test_mongo_query(mongo_collection):

    pipeline = [
        {'$match': {"project_id": TARGET_PROJECT_ID}},
        {'$group': {'_id': None, 'total_time': {'$sum': "$duration_minutes"}}}
    ]

    start_time = time.time()
    for _ in range(100):
        list(mongo_collection.aggregate(pipeline))
    end_time = time.time()

    print(f"MongoDB Aggregation Query Time: {(end_time - start_time) / 100} seconds (average)")

if __name__ == "__main__":
    mongo_collection = get_mongo_collection()
    sql_conn = get_sql_connection()
    setup_sql_master_data(sql_conn)
    mongo_collection.create_index([("project_id", 1)])

    print("\nHigh-write load test")
    test_mongo_insert(mongo_collection)
    test_sql_insert(sql_conn)

    print("\nAggregation query test")
    test_mongo_query(mongo_collection)
    test_sql_query(sql_conn)

    sql_conn.close()