from tests.conftest import create_test_user_in_db, get_user_from_db_by_id


def test_create_handler(test_client):
    username = "test_user_1"
    resp = test_client.post(f"/user/{username}")
    assert resp.status_code == 200
    data_from_resp = resp.json()
    assert data_from_resp["msg"] == "user has been created"
    user_id = data_from_resp["user_id"]
    user_from_database = get_user_from_db_by_id(user_id=user_id, db_connection=test_client.app.state.db)
    assert user_from_database[0] == user_id
    assert user_from_database[1] == username
    assert user_from_database[2] is False


def test_delete_handle(test_client):
    username = "test_user_1"
    user_id = create_test_user_in_db(username=username, db_connection=test_client.app.state.db, is_deleted=False)
    resp = test_client.delete(f"/user/{user_id}")
    assert resp.status_code == 200
    deleted_user = get_user_from_db_by_id(user_id, db_connection=test_client.app.state.db)
    assert len(deleted_user) != 0
    assert deleted_user[0] == user_id
    assert deleted_user[1] == username
    assert deleted_user[2] is True