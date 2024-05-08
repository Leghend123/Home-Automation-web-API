from flask import Flask, request
import sqlite3
from database import CREATE_ROOMS_TABLE


app = Flask(__name__)

@app.post("/api/room")
def create_room():
    data = request.get_json()
    name = data["name"]
    with sqlite3.connect("database.db") as con:
        cursor = con.cursor()
        sql_query = "INSERT INTO rooms(name) VALUES (?)"
        Rooms = CREATE_ROOMS_TABLE
        cursor.execute(Rooms)
        cursor.execute(sql_query, (name,))

        #fetch query
        sql_select_query = "SELECT * FROM rooms WHERE name = ?"
        cursor.execute(sql_select_query, (name,))
        room_id = cursor.fetchone()[0]

    return{"id": room_id, "message": f"Room {name} created."}, 201
    




