# 🏁 F1 Data Analyzer – Telemetry Viewer (FastF1 + Tkinter)

A GUI-based Python app for visualizing Formula 1 telemetry data.  
Built with FastF1, Matplotlib, and Tkinter – this tool lets you select year, track, session, driver, and graph type, and instantly see real telemetry plots in a sleek dark-mode interface.

---

## 📦 Features

- Choose year, track, session (FP/Q/S/R), driver, and graph type
- Graphs for Speed, Throttle, Brake, RPM by distance
- Color-coded based on driver's team
- Error messages for invalid input (e.g., driver not in session)
- Clean dark mode styling
- Background image (`bgF1.png`) for immersive look
- Tkinter-based GUI (not CLI!)

---

## 🛠 Tech Stack

- Language: Python 3.x
- Libraries: FastF1, Matplotlib, Pillow, Tkinter
- Graphics: Matplotlib (with FastF1 theme)
- GUI: Tkinter
- Image support: Pillow (for background)

---

## ▶️ How to Run

1. Clone or download the repository
2. Make sure `bgF1.png` is in the same directory as `main.py`
3. Install the required libraries:
```bash
pip install -r requirements.txt
```
4. Run the app (use Terminal on macOS or CMD on Windows):
```bash
python main.py
```

The window will open, and you’ll be able to explore live race data from recent seasons.


## 📁 File Structure

- main.py - The main Python app with all logic and UI
- bgF1.png - Background image for the GUI
- README.md - You're reading it!
- requirements.txt - Required Python libraries

## ✍️ Author

Created by **noairwin**  

## 🏎️ About Telemetry

Telemetry is real-time performance data collected from the car – speed, braking, RPM and more.  
This tool visualizes that data for any driver and session, making it easy to analyze what happened in every lap.
