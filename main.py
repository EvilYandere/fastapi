from fastapi import FastAPI
import uvicorn
import psycopg2
from envparse import Env


app = FastAPI()
env = Env()

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/somebase2"
#env.str("DATABASE_URL")


@app.post(path="/user/{username}")
def create_user(username: str):
    database = app.state.db
    cursor = database.cursor()
    cursor.execute("""INSERT INTO users (username, is_deleted) VALUES (%s, false) RETURNING user_id""", (username, ))
    database.commit()
    return {"msg": "user has been created",
            "user_id" : cursor.fetchone()[0]}


@app.delete(path="/user/{user_id}")
def delete_user(user_id: int):
    database = app.state.db
    cursor = database.cursor()
    cursor.execute("""UPDATE users SET is_deleted = true WHERE user_id = %s""", (user_id, ))
    database.commit()
    return {"msg": "user has been deleted"}


def create_app():
    db = psycopg2.connect(DATABASE_URL)
    app.state.db = db
    return app


if __name__ == "__main__":
    uvicorn.run(create_app())