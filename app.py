from flask import Flask, request
import sqlite3
from database import CREATE_ROOMS_TABLE, CREATE_TEMP_TABLE
from datetime import datetime, timezone



app = Flask(__name__)

#creating a room endpoint..............
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

#Addinng temperature endpoint.....................
@app.post("/api/temperature")
def add_temp():
    data = request.get_json()
    room_id = data["room"]
    temperature = data["temperature"]
    
    try:
        date = datetime.strptime(data["date"], "%m-%d-%Y %H:%M:%S")

    except KeyError:
        date = datetime.now(timezone.utc)

    with sqlite3.connect("database.db") as con:
        cursor = con.cursor()
        temp_query = "INSERT INTO temperatures(room_id, temperature, date) VALUES(?,?,?)"
        cursor.execute(temp_query, (room_id, temperature, date))

    return {"message": "Temperature added."}, 201

#Finding Average
@app.get("/api/average")
def get_average_temp():
    with sqlite3.connect("database.db") as con:
        cursor = con.cursor()
        Total_Num_Of_Days = """SELECT COUNT(DISTINCT DATE(date)) as days FROM temperatures"""
        Temp_Avg = """ SELECT AVG(temperature) as average FROM temperatures"""
        cursor.execute(Temp_Avg)
        average = cursor.fetchone()[0]
        cursor.execute(Total_Num_Of_Days)
        days = cursor.fetchone()[0]

    return {"average": round(average, 2), "days": days}

    

