import os
import fastf1
from fastf1 import plotting
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk

# cache
os.makedirs("cache", exist_ok=True)
fastf1.Cache.enable_cache('cache')
plotting.setup_mpl()

canvas = None

# set colors for every team
team_colors = {
    "Red Bull Racing": "blue",
    "Ferrari": "red",
    "Mercedes": "cyan",
    "McLaren": "orange",
    "Aston Martin": "green",
    "Williams": "deepskyblue",
    "Alpine": "magenta",
    "AlphaTauri": "purple",
    "AlphaTauri/Honda": "purple",
    "AlphaTauri RB": "purple",
    "Haas F1 Team": "white",
    "Alfa Romeo": "maroon"
}

# === GUI ===
root = tk.Tk()
root.title("Lights Out - Telemetry Analyzer")
root.geometry("1710x1190")
root.configure(bg='#121212')

# background image
bg_image = Image.open("bgF1.png")
bg_image = bg_image.resize((1710, 1190))
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# vars and put in their defults
year_var = tk.StringVar(value="2024")
track_var = tk.StringVar(value="Monaco")
session_var = tk.StringVar(value="R")
driver_var = tk.StringVar(value="VER")
graph_type_var = tk.StringVar(value="Speed")

# clear widgets
def clear_label(master, text):
    return tk.Label(master, text=text, bg=root["bg"], fg='white', font=("Arial", 10))


def clear_menu(master, variable, options):
    menu = tk.OptionMenu(master, variable, *options)
    menu.config(bg='white', fg='black', highlightthickness=0, activebackground='#ddd')
    menu['menu'].config(bg='white', fg='black')
    return menu

def clear_button(master, text, command):
    return tk.Button(
        master, text=text, command=command,
        bg=root["bg"], fg='black',
        font=("Arial", 10),
        relief='flat',
        activebackground='#1a1a1a',
        activeforeground='white',
        highlightthickness=0,
        borderwidth=0
    )


# draw a graph func
def draw_graph():
    global canvas
    year = int(year_var.get())
    track = track_var.get()
    session_type = session_var.get()
    driver_code = driver_var.get()
    graph_type = graph_type_var.get()

    try:
        session = fastf1.get_session(year, track, session_type)
        session.load()
    except Exception:
        from tkinter import messagebox
        messagebox.showerror("Error", f"Track '{track}' not found in season {year}, or an error occurred during loading.")
        return

    drivers_in_session = session.laps['Driver'].unique()
    if driver_code not in drivers_in_session:
        from tkinter import messagebox
        messagebox.showerror("Error", f"The driver '{driver_code}' did not take part in this session.")
        return

    lap = session.laps.pick_driver(driver_code).pick_fastest()
    tel = lap.get_telemetry()
    if canvas:
        canvas.get_tk_widget().destroy()

    fig = Figure(figsize=(7, 4), dpi=100)
    ax = fig.add_subplot(111)

    driver_team = lap['Team']
    color = team_colors.get(driver_team, 'white')

    unit_map = {
        "Speed": "km/h",
        "Throttle": "%",
        "Brake": "%",
        "RPM": "rpm"
    }

    ax.plot(tel['Distance'], tel[graph_type], color=color)
    ax.set_title(f"{driver_code} {graph_type} - {track} {year}", color='white')
    ax.set_xlabel("Distance (m)", color='white')
    ax.set_ylabel(f"{graph_type} ({unit_map.get(graph_type, '')})", color='white')
    ax.grid(True)

    fig.patch.set_facecolor('#1e1e1e')
    ax.set_facecolor('#2e2e2e')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('white')

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)



# main frame
main_frame = tk.Frame(root, bg=root["bg"])
main_frame.place(relx=0.5, rely=0.02, anchor='n')

for label, var, opts in [
    ("year:", year_var, ["2021", "2022", "2023", "2024"]),
    ("track:", track_var, ["Bahrain", "Hungary", "Qatar", "Monaco", "Silverstone", "Abu Dhabi", "Canada", "Saudi Arabia", "Australia", "Japan", "China", "Miami", "Emilia-Romagna", "Spain", "Austria", "Italy", "Azerbaijan", "Netherlands", "Belgium", "Singapore", "Mexico", "Brazil"]),
    ("session:", session_var, ["FP1", "FP2", "FP3", "Q", "R", "S"]),
    ("driver:", driver_var, ["VER", "LEC", "NOR", "HAM", "SAI", "PIA", "RUS", "ALB", "OCO", "GAS", "ALO", "TSU", "RIC", "HUL", "STR", "MAG", "PER", "ZHO", "SAR", "LAW", "DEV", "BOT", "SCH", "VET", "LAT", "GIO", "RAI", "MAZ"]),
    ("graph type:", graph_type_var, ["Speed", "Throttle", "Brake", "RPM"]),
]:
    clear_label(main_frame, label).pack()
    clear_menu(main_frame, var, opts).pack()


clear_button(main_frame, "Draw Graph", draw_graph).pack(pady=10)

graph_frame = tk.Frame(root, bg=root["bg"])
graph_frame.place(relx=0.5, rely=0.3, anchor='n')

root.mainloop()
