import unittest
import os
import csv
from openpyxl import load_workbook
from app import extrahuj_vysledky


from app import extrahuj_vysledky

class TestExtrakce(unittest.TestCase):
    def setUp(self):
        # Vzorek HTML podobný Google výstupu (zjednodušený)
        self.test_html = '''
        <html>
            <body>
                <div class="tF2Cxc">
                    <a href="https://example.com">
                        <h3>Příklad titulku</h3>
                    </a>
                </div>
            </body>
        </html>
        '''

    def test_extrahuj_vysledky(self):
        vysledky = extrahuj_vysledky("test", html=self.test_html)
        self.assertIsInstance(vysledky, list)
        self.assertEqual(len(vysledky), 1)
        self.assertIn("titulek", vysledky[0])
        self.assertIn("url", vysledky[0])
        self.assertEqual(vysledky[0]["titulek"], "Příklad titulku")
        self.assertEqual(vysledky[0]["url"], "https://example.com")

if __name__ == "__main__":
    unittest.main()

def test_csv_export(self):
    vysledky = extrahuj_vysledky("test", html=self.test_html)
    filename = "test_output.csv"

    # Zápis do souboru
    with open(filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["titulek", "url"])
        writer.writeheader()
        for radek in vysledky:
            writer.writerow(radek)

    # Kontrola, že soubor existuje a má obsah
    self.assertTrue(os.path.exists(filename))

    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
        self.assertGreater(len(lines), 1)  # alespoň hlavička + 1 řádek

    os.remove(filename)

def test_excel_export(self):
    vysledky = extrahuj_vysledky("test", html=self.test_html)
    filename = "test_output.xlsx"

    # Zápis do souboru
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.append(["Titulek", "URL"])
    for radek in vysledky:
        ws.append([radek["titulek"], radek["url"]])
    wb.save(filename)

    # Kontrola existence a obsahu
    self.assertTrue(os.path.exists(filename))
    wb2 = load_workbook(filename)
    sheet = wb2.active
    self.assertEqual(sheet.cell(row=2, column=1).value, "Příklad titulku")

    os.remove(filename)

