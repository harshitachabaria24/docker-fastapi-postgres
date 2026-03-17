from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.get("/health")
def health():
    return {"status": "running"}

@app.post("/users")
def add_user(name: str, email: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (name, email) VALUES (%s,%s)",
        (name, email)
    )

    conn.commit()
    cur.close()
    conn.close()

    return {"message":"User added"}

@app.get("/users")
def get_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows