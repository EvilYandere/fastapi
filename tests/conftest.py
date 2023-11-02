import os
from fastapi.testclient import TestClient
import pytest
from main import create_app, DATABASE_URL

CREATE_USER_QUERY = """
INSERT INTO users VALUES (%s, %s, %s) RETURNING user_id; 
"""

CREATE_USER_QUERY_COMMON = """
INSERT INTO users (username, is_deleted) VALUES (%s, %s) RETURNING user_id;
"""

GET_USER_BY_ID_QUERY = """
SELECT * FROM users WHERE user_id = %s;
"""


@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    print("Running migrations...")
    os.system(f"yoyo apply --database {DATABASE_URL} ./migrations -b")

#yoyo apply --database postgresql://postgres:postgres@172.19.0.2:5432/somebase2 ./migrations -b

@pytest.fixture(scope="session")
def test_client():
    with TestClient(create_app()) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def clean_tables(test_client):
    cursor = test_client.app.state.db.cursor()
    cursor.execute("""TRUNCATE TABLE users;""")
    test_client.app.state.db.commit()


def create_test_user_in_db(username:str, db_connection, is_deleted: bool = False, user_id: int = None) -> int:
    cursor = db_connection.cursor()
    if user_id is None:
        cursor.execute(CREATE_USER_QUERY_COMMON, (username, is_deleted))
    else:
        cursor.execute(CREATE_USER_QUERY, (user_id. username, is_deleted))
    db_connection.commit()
    return cursor.fetchone()[0]


def get_user_from_db_by_id(user_id: int, db_connection):
    cursor = db_connection.cursor()
    cursor.execute(GET_USER_BY_ID_QUERY, (user_id, ))
    return cursor.fetchone()
