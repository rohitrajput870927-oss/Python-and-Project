# weather_dashboard_weatherapi.py
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import threading
import requests
from io import BytesIO
from PIL import Image, ImageTk

# ---------- CONFIG ----------
# You provided this example key/URL. Replace with your own key if you want.
WEATHERAPI_KEY = "b2371a6c6e90466eb00180018250510"
DEFAULT_CITY = "London"
TIMEOUT = 10  # seconds for HTTP requests

# ---------- HELPERS: WeatherAPI ----------
def fetch_weatherapi_forecast(city, days=7):
    """
    Calls WeatherAPI forecast endpoint:
    https://api.weatherapi.com/v1/forecast.json?key=KEY&q=CITY&days=7&aqi=yes&alerts=yes
    Returns parsed JSON or raises requests exceptions / ValueError.
    """
    base = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": WEATHERAPI_KEY,
        "q": city,
        "days": days,
        "aqi": "yes",
        "alerts": "yes"
    }
    r = requests.get(base, params=params, timeout=TIMEOUT)
    r.raise_for_status()
    data = r.json()
    if "location" not in data or "current" not in data:
        raise ValueError("Invalid response from WeatherAPI")
    return data

def _safe_icon_url(icon_str):
    """WeatherAPI returns icon like //cdn.weatherapi.com/..., ensure it has scheme."""
    if not icon_str:
        return None
    if icon_str.startswith("//"):
        return "https:" + icon_str
    if icon_str.startswith("http"):
        return icon_str
    return "https://" + icon_str.lstrip("/")

# ---------- GUI ----------
class WeatherDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard (WeatherAPI)")
        self.root.geometry("920x720")
        self.root.configure(bg="#0b1b2b")
        self.icon_img = None
        self._build_ui()
        # initial load
        self.city_var.set(DEFAULT_CITY)
        self.fetch_weather_async()

    def _build_ui(self):
        top = tk.Frame(self.root, bg="#0b1b2b")
        top.pack(fill="x", pady=8)

        tk.Label(top, text="City:", bg="#0b1b2b", fg="white", font=("Segoe UI", 11)).pack(side="left", padx=(10,4))
        self.city_var = tk.StringVar()
        self.city_entry = tk.Entry(top, textvariable=self.city_var, width=24, font=("Segoe UI", 11))
        self.city_entry.pack(side="left")
        tk.Button(top, text="Get Weather", command=self.fetch_weather_async,
                  bg="#1f6feb", fg="white", relief="flat", font=("Segoe UI", 10)).pack(side="left", padx=8)

        self.last_update_lbl = tk.Label(top, text="", bg="#0b1b2b", fg="#b7c6d9", font=("Segoe UI", 10))
        self.last_update_lbl.pack(side="right", padx=10)

        # Current block
        curr = tk.LabelFrame(self.root, text="Current Weather", bg="#071126", fg="white", font=("Segoe UI", 11, "bold"))
        curr.pack(fill="x", padx=12, pady=(6,12))

        self.temp_lbl = tk.Label(curr, text="--°C", bg="#071126", fg="#ffd86b", font=("Segoe UI", 36, "bold"))
        self.temp_lbl.grid(row=0, column=0, padx=12, pady=10, sticky="w")

        self.icon_lbl = tk.Label(curr, bg="#071126")
        self.icon_lbl.grid(row=0, column=1, rowspan=2, padx=6)

        self.cond_lbl = tk.Label(curr, text="--", bg="#071126", fg="white", font=("Segoe UI", 14, "bold"))
        self.cond_lbl.grid(row=0, column=2, padx=8, sticky="w")

        self.loc_time_lbl = tk.Label(curr, text="", bg="#071126", fg="#b7c6d9", font=("Segoe UI", 10))
        self.loc_time_lbl.grid(row=1, column=0, padx=12, sticky="w")

        # metrics grid
        metrics = tk.Frame(self.root, bg="#071126")
        metrics.pack(fill="x", padx=12, pady=(0,8))
        self.metrics = {}
        keys = ["Humidity", "Wind", "UV", "Precip", "Pressure", "Visibility", "Sunrise", "Sunset", "AQI"]
        for i, k in enumerate(keys):
            lbl = tk.Label(metrics, text=f"{k}: --", bg="#083047", fg="#dbeafe", font=("Segoe UI", 10), width=30, anchor="w", padx=6, pady=6, relief="flat")
            lbl.grid(row=i//2, column=i%2, padx=6, pady=4, sticky="w")
            self.metrics[k] = lbl

        # Notebook for forecasts
        self.notebook = ttk.Notebook(self.root)
        self.hourly_frame = tk.Frame(self.notebook, bg="#071126")
        self.daily_frame = tk.Frame(self.notebook, bg="#071126")
        self.notebook.add(self.hourly_frame, text="Hourly (next 24h)")
        self.notebook.add(self.daily_frame, text="Daily (7 days)")
        self.notebook.pack(fill="both", expand=True, padx=12, pady=10)

        # Hourly container (scrollable horizontally)
        self.hourly_canvas = tk.Canvas(self.hourly_frame, bg="#071126", height=170, highlightthickness=0)
        self.hourly_scroll = tk.Scrollbar(self.hourly_frame, orient="horizontal", command=self.hourly_canvas.xview)
        self.hourly_inner = tk.Frame(self.hourly_canvas, bg="#071126")
        self.hourly_canvas.create_window((0,0), window=self.hourly_inner, anchor="nw")
        self.hourly_canvas.config(xscrollcommand=self.hourly_scroll.set)
        self.hourly_canvas.pack(fill="both", expand=True, side="top")
        self.hourly_scroll.pack(fill="x", side="bottom")
        self.hourly_inner.bind("<Configure>", lambda e: self.hourly_canvas.config(scrollregion=self.hourly_canvas.bbox("all")))

        # Daily container
        self.daily_list = tk.Frame(self.daily_frame, bg="#071126")
        self.daily_list.pack(fill="both", expand=True)

    def set_status(self, text):
        self.last_update_lbl.config(text=text)

    def fetch_weather_async(self):
        threading.Thread(target=self._fetch_weather, daemon=True).start()

    def _fetch_weather(self):
        city = self.city_var.get().strip() or DEFAULT_CITY
        self.set_status("Fetching...")
        try:
            data = fetch_weatherapi_forecast(city, days=7)
        except requests.HTTPError as he:
            self.root.after(0, lambda: messagebox.showerror("API Error", f"HTTP error: {he}"))
            self.set_status("Ready")
            return
        except requests.RequestException:
            self.root.after(0, lambda: messagebox.showerror("Network Error", "Cannot reach WeatherAPI."))
            self.set_status("Ready")
            return
        except ValueError as ve:
            self.root.after(0, lambda: messagebox.showerror("API Error", str(ve)))
            self.set_status("Ready")
            return

        # update UI in main thread
        self.root.after(0, lambda: self._update_ui_with_weatherapi(data))

    def _update_ui_with_weatherapi(self, data):
        try:
            location = data.get("location", {})
            cur = data.get("current", {})
            forecast = data.get("forecast", {})
            # Basic location/time
            loc_name = f"{location.get('name','--')}, {location.get('country','--')}"
            localtime = location.get("localtime", "")
            self.loc_time_lbl.config(text=f"{loc_name} | Local: {localtime}")

            # Current temp & condition
            temp_c = cur.get("temp_c", None)
            self.temp_lbl.config(text=f"{temp_c:.1f}°C" if temp_c is not None else "--")
            cond = cur.get("condition", {}).get("text", "--")
            self.cond_lbl.config(text=cond)

            # Icon
            icon_url = _safe_icon_url(cur.get("condition", {}).get("icon", ""))
            if icon_url:
                try:
                    r = requests.get(icon_url, timeout=5)
                    r.raise_for_status()
                    img = Image.open(BytesIO(r.content)).resize((80,80))
                    self.icon_img = ImageTk.PhotoImage(img)
                    self.icon_lbl.config(image=self.icon_img)
                except Exception:
                    self.icon_lbl.config(image="")
            else:
                self.icon_lbl.config(image="")

            # Metrics
            self.metrics["Humidity"].config(text=f"Humidity: {cur.get('humidity','--')} %")
            wind_kph = cur.get("wind_kph", 0)
            wind_dir = cur.get("wind_dir", "--")
            self.metrics["Wind"].config(text=f"Wind: {wind_kph:.1f} kph, {wind_dir}")
            uvi = cur.get("uv", None)
            self.metrics["UV"].config(text=f"UV: {uvi:.1f}" if uvi is not None else "UV: --")
            precip_mm = cur.get("precip_mm", None)
            self.metrics["Precip"].config(text=f"Precip: {precip_mm} mm" if precip_mm is not None else "Precip: --")
            self.metrics["Pressure"].config(text=f"Pressure: {cur.get('pressure_mb','--')} mb")
            vis_km = cur.get("vis_km", None)
            self.metrics["Visibility"].config(text=f"Visibility: {vis_km:.1f} km" if vis_km is not None else "Visibility: --")
            # AQI (if available)
            aqi_str = "--"
            if "air_quality" in cur and cur["air_quality"]:
                # WeatherAPI returns an 'air_quality' dict with keys like "pm2_5", "pm10", "us-epa-index"
                aq = cur["air_quality"]
                # Pick the us-epa-index if present
                aqi_idx = aq.get("us-epa-index")
                if aqi_idx is not None:
                    aqi_str = f"US EPA: {aqi_idx}"
                else:
                    aqi_str = f"PM2.5: {aq.get('pm2_5','--')}"
            self.metrics["AQI"].config(text=f"AQI: {aqi_str}")

            # Sunrise/Sunset are inside forecast -> forecastday[0].astro
            forecast_days = forecast.get("forecastday", [])
            if forecast_days:
                astro = forecast_days[0].get("astro", {})
                self.metrics["Sunrise"].config(text=f"Sunrise: {astro.get('sunrise','--')}")
                self.metrics["Sunset"].config(text=f"Sunset: {astro.get('sunset','--')}")
            else:
                self.metrics["Sunrise"].config(text="Sunrise: --")
                self.metrics["Sunset"].config(text="Sunset: --")

            # Hourly: use forecastday[0].hour list (hours are local)
            for w in self.hourly_inner.winfo_children():
                w.destroy()
            hourly_all = []
            if forecast_days:
                hourly_all = forecast_days[0].get("hour", [])  # list of 24 items for the day
            # If we want next 24 hours including remainder of current day and next day, we can combine
            # Here we'll take up to 24 items starting from current hour index based on localtime hour
            current_local_hour = int(location.get("localtime", datetime.now().strftime("%Y-%m-%d %H:%M")).split(" ")[1].split(":")[0])
            # flatten hours from day 0 and day1 if needed
            all_hours = []
            for fd in forecast_days[:2]:
                all_hours.extend(fd.get("hour", []))
            # find index of current hour in all_hours (match on hour dt)
            idx = 0
            if all_hours:
                # find first hour where its hour matches current_local_hour AND its date matches today
                # fallback: start from 0
                for i, h in enumerate(all_hours):
                    try:
                        dt_str = h.get("time")  # format "2025-12-02 15:00"
                        hhour = int(dt_str.split(" ")[1].split(":")[0])
                        if hhour == current_local_hour:
                            idx = i
                            break
                    except:
                        continue
            slice_hours = all_hours[idx: idx + 24]
            for i, h in enumerate(slice_hours):
                frame = tk.Frame(self.hourly_inner, bg="#071126", bd=1, relief="ridge", padx=6, pady=6)
                frame.grid(row=0, column=i, padx=4, pady=6)
                t = h.get("time", "").split(" ")[1] if h.get("time") else "--:--"
                tk.Label(frame, text=t, bg="#071126", fg="#e6eef8", font=("Segoe UI",9)).pack()
                temp_h = h.get("temp_c", None)
                tk.Label(frame, text=f"{temp_h:.0f}°C" if temp_h is not None else "--", bg="#071126", fg="#ffd86b", font=("Segoe UI",11,"bold")).pack()
                icon_h = _safe_icon_url(h.get("condition", {}).get("icon", ""))
                if icon_h:
                    try:
                        r = requests.get(icon_h, timeout=5)
                        r.raise_for_status()
                        im = Image.open(BytesIO(r.content)).resize((40,40))
                        imgtk = ImageTk.PhotoImage(im)
                        lbl = tk.Label(frame, image=imgtk, bg="#071126")
                        lbl.image = imgtk
                        lbl.pack()
                    except:
                        pass
                # chance of rain (WeatherAPI provides chance_of_rain and chance_of_snow)
                cop = h.get("chance_of_rain", None) or h.get("chance_of_snow", None)
                if cop is not None:
                    tk.Label(frame, text=f"{int(cop)}%", bg="#071126", fg="#c6dafe", font=("Segoe UI",9)).pack()

            # Daily list: forecastday entries
            for w in self.daily_list.winfo_children():
                w.destroy()
            for d in forecast_days[:7]:
                date_str = d.get("date")
                day = d.get("day", {})
                tmin = day.get("mintemp_c", None)
                tmax = day.get("maxtemp_c", None)
                desc_d = day.get("condition", {}).get("text", "--")
                frame = tk.Frame(self.daily_list, bg="#071126", pady=6)
                frame.pack(fill="x", padx=6)
                tk.Label(frame, text=date_str, width=18, anchor="w", bg="#071126", fg="#e6eef8", font=("Segoe UI",10,"bold")).pack(side="left")
                tk.Label(frame, text=f"{tmin:.0f}° / {tmax:.0f}°" if tmin is not None and tmax is not None else "--", width=14, anchor="w", bg="#071126", fg="#ffd86b", font=("Segoe UI",10)).pack(side="left")
                tk.Label(frame, text=desc_d, anchor="w", bg="#071126", fg="#cfe8ff", font=("Segoe UI",10)).pack(side="left", padx=8)

            now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.set_status(f"Updated: {now} (WeatherAPI)")
        except Exception as e:
            messagebox.showerror("UI Error", f"Failed to update UI: {e}")
            self.set_status("Ready")

if __name__ == "__main__":
    if not WEATHERAPI_KEY or WEATHERAPI_KEY.strip() == "":
        tk.Tk().withdraw()
        messagebox.showwarning("API Key missing", "Set WEATHERAPI_KEY variable in the script with your WeatherAPI key.")
    root = tk.Tk()
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except:
        pass
    app = WeatherDashboard(root)
    root.mainloop()
