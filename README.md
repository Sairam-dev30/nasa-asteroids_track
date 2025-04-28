# 🚀 NASA Asteroid Tracker

This project fetches Near Earth Object (NEO) data from the NASA API and stores it into a MySQL database.  
You can interactively **filter**, **analyze**, and **visualize** asteroid data using a beautiful **Streamlit web app**!

---

## 📦 Features

- ✅ Fetch Asteroid Data from NASA's NEO API
- ✅ Store structured asteroid data in MySQL
- ✅ Interactive Streamlit dashboard
- ✅ Filter asteroids based on:
  - Magnitude
  - Diameter
  - Velocity
  - Distance
  - Hazardous status
  - Approach dates
- ✅ Pre-built quick queries (Top 5 largest, fastest, hazardous, closest asteroids)
- ✅ Modern and responsive UI

---

## ⚙️ Installation

1. Clone this repository or download the ZIP:
   ```bash
   git clone https://github.com/your-username/nasa-asteroid-tracker.git
   cd nasa-asteroid-tracker
2.Install Python packages:
pip install -r requirements.txt
3.Setup your MySQL database:
*Create a database named astro
*Update your MySQL username and password inside both fetch_asteroids.py and app.py
4.Fetch asteroid data:
bash

python fetch_asteroids.py
5.Run the Streamlit web app:
bash
streamlit run app.py
🗂 Project Structure
bash
nasa-asteroid-tracker/
│
├── fetch_asteroids.py   # Fetch data from NASA API and insert into MySQL
├── app.py               # Streamlit app for visualization
├── requirements.txt     # Python dependencies
├── .gitignore           # Files to ignore in GitHub
└── README.md            # Project documentation
🚀 Credits
NASA NEO API - https://api.nasa.gov/
Built with 💖 by Sairam
📜 License
This project is open-source and free to use.
Feel free to fork, modify, and build amazing things!
