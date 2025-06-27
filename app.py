from flask import Flask, request, send_file, render_template
import requests
from bs4 import BeautifulSoup
import csv
import time
import os
from openpyxl import Workbook

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

def extrahuj_vysledky(dotaz, html=None):
    if html is None:
        query = dotaz.replace(" ", "+")
        url = f"https://www.google.com/search?q={query}&hl=cs"
        response = requests.get(url, headers=HEADERS)
        html = response.text  # jen pokud není html předáno

    soup = BeautifulSoup(html, "html.parser")

    vysledky = []
    for item in soup.select('div.tF2Cxc'):
        nadpis = item.select_one('h3')
        odkaz = item.select_one('a')
        if nadpis and odkaz:
            vysledky.append({
                "titulek": nadpis.text.strip(),
                "url": odkaz['href']
            })
    return vysledky

@app.route("/")
def home():
    return render_template("formular.html")

@app.route("/vyhledat", methods=["GET", "POST"])
def vyhledat():
    if request.method == "GET":
        return "Tato adresa slouží pouze pro odeslání formuláře (POST)."

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
    else:
        filename = f"vysledky_{timestamp}.csv"
        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["titulek", "url"])
            writer.writeheader()
            for radek in vysledky:
                writer.writerow(radek)

    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
