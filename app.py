from flask import Flask, request, send_file, render_template
import requests
import csv
import time
import os
from openpyxl import Workbook
from dotenv import load_dotenv

load_dotenv()  # Načte proměnné z .env

app = Flask(__name__)

def extrahuj_vysledky(dotaz):
    api_key = os.getenv("SERPAPI_KEY")
    params = {
        "engine": "google",
        "q": dotaz,
        "hl": "cs",
        "api_key": api_key
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    vysledky = []
    for result in data.get("organic_results", []):
        vysledky.append({
            "titulek": result.get("title", ""),
            "url": result.get("link", "")
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
