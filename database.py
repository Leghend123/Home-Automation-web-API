import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

CREATE_ROOMS_TABLE = """CREATE TABLE IF NOT EXISTS rooms(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)"""
cursor.execute(CREATE_ROOMS_TABLE)
conn.commit()
print("created rooms successfully")    

CREATE_TEMP_TABLE = """CREATE TABLE IF NOT EXISTS temperatures(room_id, temperature REAL, date TIMESTAMP, FOREIGN KEY(room_id) REFERENCES rooms(id) ON DELETE CASCADE)"""
cursor.execute(CREATE_TEMP_TABLE)
conn.commit()
print("created temperature successfully")


conn.close()
