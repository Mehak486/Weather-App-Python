import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk, ImageFilter
from io import BytesIO

API_KEY = "e089d0b5c7c51c1820e34fb4d3b2ee3b"

# ------------------ WEATHER API ------------------
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    if res.status_code != 200:
        return None
    d = res.json()
    return {
        "city": d["name"],
        "temp": round(d["main"]["temp"]),
        "feels": round(d["main"]["feels_like"]),
        "desc": d["weather"][0]["description"].title(),
        "icon": d["weather"][0]["icon"],
        "wind": d["wind"]["speed"],
        "humidity": d["main"]["humidity"],
        "pressure": d["main"]["pressure"]
    }

# ------------------ WEATHER SEARCH ------------------
def search_weather():
    city = city_entry.get()
    w = get_weather(city)
    if not w:
        status_lbl.config(text="❌ City not found")
        return

    status_lbl.config(text="")
    city_lbl.config(text=w["city"])
    temp_lbl.config(text=f"{w['temp']}°C")
    desc_lbl.config(text=f"{w['desc']} | Feels like {w['feels']}°C")
    wind_val.config(text=f"{w['wind']} m/s")
    hum_val.config(text=f"{w['humidity']}%")
    pres_val.config(text=f"{w['pressure']} hPa")

    # Weather Icon with Shadow
    icon_url = f"http://openweathermap.org/img/wn/{w['icon']}@2x.png"
    img = Image.open(BytesIO(requests.get(icon_url).content)).resize((130, 130))
    shadow = img.convert("RGBA").filter(ImageFilter.GaussianBlur(5))
    shadow_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
    shadow_img.paste(shadow, (5, 5))
    shadow_img.paste(img, (0, 0), img)
    icon_img = ImageTk.PhotoImage(shadow_img)
    icon_lbl.config(image=icon_img)
    icon_lbl.image = icon_img

# ------------------ ROUND RECTANGLE FUNCTION ------------------
def round_rectangle(canvas, x1, y1, x2, y2, r=25, **kwargs):
    # Draw 4 corner arcs
    canvas.create_arc(x1, y1, x1+r*2, y1+r*2, start=90, extent=90, style='pieslice', **kwargs)
    canvas.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90, style='pieslice', **kwargs)
    canvas.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, style='pieslice', **kwargs)
    canvas.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, style='pieslice', **kwargs)
    
    # Draw rectangles between arcs
    canvas.create_rectangle(x1+r, y1, x2-r, y2, **kwargs)
    canvas.create_rectangle(x1, y1+r, x2, y2-r, **kwargs)

# ------------------ WINDOW ------------------
root = tk.Tk()
root.title("Weather App")
root.geometry("440x650")
root.resizable(False, False)

# ------------------ GRADIENT BACKGROUND ------------------
canvas = tk.Canvas(root, width=440, height=650, highlightthickness=0)
canvas.pack(fill="both", expand=True)
for i in range(650):
    r = int(110 + (255-110) * (i/650))
    g = int(198 + (255-198) * (i/650))
    b = 255
    color = f'#{r:02x}{g:02x}{b:02x}'
    canvas.create_line(0, i, 440, i, fill=color)

# ------------------ SEARCH FRAME ------------------
search_frame = tk.Frame(root, bg="#6EC6FF")
canvas.create_window(220, 40, window=search_frame)

city_entry = tk.Entry(search_frame, font=("Segoe UI", 14),
                      width=20, justify="center", bd=0)
city_entry.insert(0, "London")
city_entry.pack(side="left", ipady=6)

search_btn = tk.Button(search_frame, text="🔍", font=("Segoe UI", 14),
                       bg="#007ACC", fg="white", bd=0,
                       command=search_weather)
search_btn.pack(side="left", padx=8, ipady=4)

status_lbl = tk.Label(root, text="", bg="#6EC6FF", fg="red")
canvas.create_window(220, 80, window=status_lbl)

# Hover effect
def on_enter(e): search_btn.config(bg="#005999")
def on_leave(e): search_btn.config(bg="#007ACC")
search_btn.bind("<Enter>", on_enter)
search_btn.bind("<Leave>", on_leave)

# ------------------ MAIN CARD ------------------
card_frame = tk.Frame(root, bg="#ffffff", bd=0)
canvas.create_window(220, 360, window=card_frame, width=380, height=440)

card_canvas = tk.Canvas(card_frame, width=380, height=440, bg="#ffffff", highlightthickness=0)
card_canvas.pack(fill="both", expand=True)
round_rectangle(card_canvas, 10, 10, 370, 430, r=25, fill="#ffffff", outline="#ffffff", width=2)

icon_lbl = tk.Label(card_frame, bg="#ffffff")
icon_lbl.place(x=125, y=20)

temp_lbl = tk.Label(card_frame, text="--°C", font=("Segoe UI", 40, "bold"), bg="#ffffff")
temp_lbl.place(x=120, y=160)

city_lbl = tk.Label(card_frame, text="City", font=("Segoe UI", 22, "bold"), bg="#ffffff")
city_lbl.place(x=140, y=220)

desc_lbl = tk.Label(card_frame, text="", font=("Segoe UI", 12), bg="#ffffff")
desc_lbl.place(x=80, y=260)

# ------------------ INFO CARDS ------------------
info_frame = tk.Frame(card_frame, bg="#ffffff")
info_frame.place(x=40, y=300)

def info_card(icon, title):
    f = tk.Frame(info_frame, bg="#E3F2FD", width=95, height=80)
    f.pack(side="left", padx=8)
    f.pack_propagate(False)
    tk.Label(f, text=icon, font=("Segoe UI Emoji", 18), bg="#E3F2FD").pack()
    tk.Label(f, text=title, font=("Segoe UI", 9, "bold"), bg="#E3F2FD").pack()
    val = tk.Label(f, text="--", font=("Segoe UI", 11, "bold"), bg="#E3F2FD")
    val.pack()
    return val

wind_val = info_card("🌬️", "WIND")
hum_val = info_card("💧", "HUMIDITY")
pres_val = info_card("⏱️", "PRESSURE")

# ------------------ START ------------------
search_weather()
root.mainloop()
