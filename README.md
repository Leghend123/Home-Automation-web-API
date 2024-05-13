# Home-Automation-web-API
Home automation web service to retrieve and store temperature in different room of your house. this leverage on flask to build an API to get the temperatures of the rooms

-Real-time collection of temperature readings from IoT devices enables continuous monitoring and analysis of temperature variations in various environments. By leveraging sensors connected to IoT networks, temperature data can be gathered remotely and instantaneously.

-QUICKSTART..............
Create a .env file with a SQLite database. Look at .env.example for information on how this should be written.

Create a Python virtual environment:
 - python3.10 -m venv .venv

Activate the virtual environment and install the dependencies using pip:
- source .venv/bin/activate  # different on Windows

 -pip install -r requirements.txt
Run the app:
- flask run

ENDPOINTS............
- @app.post("/api/room")
- @app.post("/api/temperature")
- @app.get("/api/average")
- @app.get("/api/room/<int:room_id>")