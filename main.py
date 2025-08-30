import os
import requests
from atproto import Client

URL = "https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/c6e9f744-4dbf-4e8e-a219-cab051ec610c.json?includeTimeseries=true&includeCurrentMeasurement=true"

BLUESKY_USER = os.getenv("BLUESKY_USER")
BLUESKY_PASS = os.getenv("BLUESKY_PASS")

def get_wasserstand():
    resp = requests.get(URL)
    data = resp.json()
    measurement = data["timeseries"][0]["currentMeasurement"]
    wert = measurement["value"]
    zeit = measurement["timestamp"]
    return wert, zeit

def post_bluesky(text):
    client = Client()
    client.login(BLUESKY_USER, BLUESKY_PASS)
    client.send_post(text)

def main():
    wert, zeit = get_wasserstand()
    text = f"🌊 Aktueller Wasserstand Edersee: {wert} m (Stand: {zeit})"
    print("Posting:", text)
    post_bluesky(text)

if __name__ == "__main__":
    main()
