Hi, Nikhil

🧭 Task: Build a Basic Routing System (with Google OR-Tools)
You're going to build a multi-route delivery system using:

📍 Node.js – for generating coordinates, triggering routing logic, and serving the UI

🐍 Python (Google OR-Tools) – to calculate optimized delivery routes

💻 Bootstrap – for a simple, clean frontend

🎯 Goal:
Generate ~30 random coordinates in a defined area

Create 3 optimized delivery routes

All routes should start from the same fixed starting point (e.g., a shop location)

🔧 Tech Breakdown:
Backend:
Use Node.js to:

Generate random coordinates (within a city)

Save them to a file or pass to Python

Run a Python script using child_process

Collect the routes from Python output (JSON or stdout)

Routing:
Use Google OR-Tools in Python:

Solve the Vehicle Routing Problem (VRP)

Use 3 vehicles, each with its route starting from the same depot

Return the list of stops for each route in order

Frontend:
Use Bootstrap to display:

3 separate routes

Stops listed for each route

The starting point clearly indicated

📚 References:
Google OR-Tools VRP: https://developers.google.com/optimization/routing/vrp

Use Python’s OR-Tools via pip install ortools

For running Python in Node: child_process.exec guide

Let me know if you face any issues installing OR-Tools or integrating Python with Node. Looking forward to your update!