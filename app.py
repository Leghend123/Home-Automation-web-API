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


#Finding Average temperature from specific room
@app.get("/api/room/<int:room_id>")
def get_all_room(room_id):
    args = request.args
    term = args.get("term")
    if term is not None:
        return get_room_term(room_id, term)
    else:
        with sqlite3.connect("database.db") as con:
            cursor = con.cursor()
            Room_Name_Query = """ SELECT name FROM rooms WHERE id = (?) """
            Room_Days_Query = """ SELECT COUNT(DISTINCT DATE(date)) as days FROM temperatures WHERE room_id = (?) """
            Room_All_Time_Avg_Temp = """ SELECT AVG(temperature) as average FROM temperatures WHERE room_id = (?)"""
            cursor.execute(Room_Name_Query, (room_id,))
            Room_Name = cursor.fetchone()[0]
            cursor.execute(Room_Days_Query, (room_id,))
            Room_Days = cursor.fetchone()[0]
            cursor.execute(Room_All_Time_Avg_Temp, (room_id,))
            Room_Avg_temp = cursor.fetchone()[0]
        return {
              "Room Name": Room_Name,
              "Days":Room_Days, 
              "Room Average Temp": Room_Avg_temp
        }


#function for terms at which users can search from the temperature Avg about room....
def get_room_term(room_id,term):
    terms = {"week":7, "month":30}
    with sqlite3.connect("database.db") as con:
        cursor = con.cursor()
        Room_Terms_Query = """SELECT DATE(temperatures.date) as reading_date,AVG(temperatures.temperature)FROM temperatures WHERE temperatures.room_id = (%s)GROUP BY reading_date HAVING DATE(temperatures.date) > (SELECT MAX(DATE(temperatures.date))-(%s) FROM temperatures);"""
        Room_Name_Query = """ SELECT name FROM rooms WHERE id = (?) """
        cursor.execute(Room_Name_Query,(room_id,))
        Room_Name = cursor.fetchone()[0]
        cursor.execute(Room_Terms_Query,(room_id, terms[term]))
        Dates_Of_Temperatures = cursor.fetchone()[0]
        Average = sum(day[1] for day in Dates_Of_Temperatures) / len(Dates_Of_Temperatures)
    return {
        "Roon Name": Room_Name,
        "temperatures": Dates_Of_Temperatures,
        "average": round(Average, 2),
    }

