import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
from requests import Session
import os
from dotenv import load_dotenv

#Load environment variables from .env
load_dotenv()
USERNAME = os.getenv("SPACE_TRACK_USERNAME")
PASSWORD = os.getenv("SPACE_TRACK_PASSWORD")

#TLE Parsing Function
def parse_tle(tle_lines):
    if len(tle_lines) < 2:
        raise ValueError("Incomplete TLE data received.")

    line1 = tle_lines[0]
    line2 = tle_lines[1]

    return {
        'Satellite Number': line1[2:7],
        'Epoch Year': line1[18:20],
        'Epoch (Day of Year and fractional)': line1[20:32],
        'First Derivative of Mean Motion': line1[33:43],
        'Second Derivative of Mean Motion': line1[44:52],
        'BSTAR drag term': line1[53:61],
        'Inclination (deg)': line2[8:16],
        'RAAN (deg)': line2[17:25],
        'Eccentricity': '0.' + line2[26:33],
        'Argument of Perigee (deg)': line2[34:42],
        'Mean Anomaly (deg)': line2[43:51],
        'Mean Motion (rev/day)': line2[52:63],
        'Revolution Number': line2[63:68]
    }

#Space-Track Fetch Function
def get_tle(norad_id):
    with Session() as session:
        login_url = 'https://www.space-track.org/ajaxauth/login'
        query_url = f'https://www.space-track.org/basicspacedata/query/class/tle_latest/NORAD_CAT_ID/{norad_id}/orderby/epoch desc/limit/1/format/tle'

        login_response = session.post(login_url, data={'identity': USERNAME, 'password': PASSWORD})
        if login_response.status_code != 200:
            return None

        tle_response = session.get(query_url)
        if tle_response.status_code == 200 and tle_response.text.strip():
            tle_lines = tle_response.text.strip().split('\n')
            return tle_lines
        else:
            return None

#GUI Callback
def fetch_and_parse():
    norad_id = entry.get().strip()
    if not norad_id.isdigit():
        messagebox.showerror("Input Error", "Please enter a valid NORAD ID.")
        return

    tle = get_tle(norad_id)
    if tle and len(tle) >= 2:
        try:
            parsed = parse_tle(tle)
            output_text.delete('1.0', tk.END)
            output_text.insert(tk.END, f"TLE:\n{tle[0]}\n{tle[1]}\n\nParsed TLE:\n")
            for key, value in parsed.items():
                output_text.insert(tk.END, f"{key}: {value}\n")
        except Exception as e:
            messagebox.showerror("Parsing Error", str(e))
    else:
        messagebox.showerror("Error", "TLE not found or Space-Track login failed.")

#GUI Setup
root = tk.Tk()
root.title("TLE Parser by NORAD ID")

tk.Label(root, text="Enter NORAD ID:").pack(pady=5)
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

tk.Button(root, text="Fetch and Parse TLE", command=fetch_and_parse).pack(pady=10)

output_text = scrolledtext.ScrolledText(root, width=80, height=20)
output_text.pack(padx=10, pady=10)

root.mainloop()
