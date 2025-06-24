

from flask import Flask, request, send_file
import requests
from bs4 import BeautifulSoup
import csv
import time
import os
from openpyxl import Workbook

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def extrahuj_vysledky(dotaz):
    query = dotaz.replace(" ", "+")
    url = f"https://www.google.com/search?q={query}&hl=cs"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    vysledky = []
    for item in soup.select('div.g'):
        nadpis = item.select_one('h3')
        odkaz = item.select_one('a')
        if nadpis and odkaz:
            vysledky.append({
                "titulek": nadpis.text.strip(),
                "url": odkaz['href']
            })
    return vysledky

@app.route("/vyhledat", methods=["POST"])
def vyhledat():
    dotaz = request.form["dotaz"]
    format = request.form["format"]
    vysledky = extrahuj_vysledky(dotaz)
    timestamp = int(time.time())

    if format == "excel":
        filename = f"vysledky_{timestamp}.xlsx"
        wb = Workbook()
        ws = wb.active
        ws.append(["Titulek", "URL"])
        for radek in vysledky:
            ws.append([radek["titulek"], radek["url"]])
        wb.save(filename)
    else:  # CSV jako výchozí
        filename = f"vysledky_{timestamp}.csv"
        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["titulek", "url"])
            writer.writeheader()
            for radek in vysledky:
                writer.writerow(radek)

    return send_file(filename, as_attachment=True)

@app.route("/")
def home():
    return "Aplikace běží"

@app.route("/vyhledat", methods=["GET", "POST"])
def vyhledat():
    if request.method == "GET":
        return "Tato adresa slouží pouze pro odeslání formuláře (POST)."

if __name__ == "__main__":
    app.run(debug=True)
