import os
import requests
from atproto import Client

URL = "https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/c6e9f744-4dbf-4e8e-a219-cab051ec610c.json?includeTimeseries=true&includeCurrentMeasurement=true"

BLUESKY_USER = os.getenv("BLUESKY_USER")
BLUESKY_PASS = os.getenv("BLUESKY_PASS")

FUELLSTANDSTABELLE = {
207: 0.25,
208: 0.50,
209: 0.75,
210: 1.25,
211: 2.00,
212: 2.75,
213: 3.40,
214: 4.78,
215: 5.93,
216: 7.20,
217: 8.66,
218: 10.25,
219: 11.87,
220: 13.58,
221: 15.41,
222: 17.36,
223: 19.41,
224: 21.60,
225: 23.91,
226: 26.34,
227: 28.89,
228: 31.54,
229: 34.28,
230: 37.13,
231: 40.10,
232: 43.21,
233: 46.49,
234: 49.95,
235: 53.58,
236: 57.35,
237: 61.30,
238: 65.45,
239: 69.81,
240: 74.33,
241: 79.04,
242: 83.98,
243: 89.13,
244: 94.49,
245: 99.83,
245: 100.00
}


def get_wasserstand():
    resp = requests.get(URL)
    data = resp.json()
    measurement = data["timeseries"][0]["currentMeasurement"]
    wert = measurement["value"]
    zeit = measurement["timestamp"]
    return wert, zeit

def berechne_fuellstand(pegel, tabelle):
    pegelmeter = sorted(tabelle.keys())
    if pegel <= pegelmeter[0]:
        return tabelle[pegelmeter[0]]
    if pegel >= pegelmeter[-1]:
        return tabelle[pegelmeter[-1]]
    
    for i in range(len(pegelmeter) - 1):
        unten = pegelmeter[i]
        oben = pegelmeter[i + 1]
        if unten <= pegel <= oben:
            fuell_unten = tabelle[unten]
            fuell_oben = tabelle[oben]
            # Lineare Interpolation
            anteil = (pegel - unten) / (oben - unten)
            fuellstand = fuell_unten + anteil * (fuell_oben - fuell_unten)
            return round(fuellstand, 1)
    
    # Falls keine passende Stelle gefunden wird (sollte nicht passieren)
    return None

def post_bluesky(text):
    client = Client()
    client.login(BLUESKY_USER, BLUESKY_PASS)
    client.send_post(text)

from datetime import datetime

def main():
    wert, zeit = get_wasserstand()
    # ISO-String in datetime-Objekt umwandeln
    dt = datetime.fromisoformat(zeit)
    # Schönes Format: 30.08.2025 um 21:30 Uhr
    zeit_formatiert = dt.strftime("%d.%m.%Y um %H:%M Uhr")
    
    text = f"🌊 Wasserstand Edersee: {wert.2f}m über NN ({zeit_formatiert})\n"
    text += f"🪣 Füllstand: {fuellstand:.1f}%"
    
    print("Posting:", text)
    post_bluesky(text)

if __name__ == "__main__":
    main()
