# cameras
#  Pametni prikaz zemljevida z vremenskimi in video podatki

Projektna spletna aplikacija, razvita z uporabo **Flask (Python)**, prikazuje interaktivni zemljevid Slovenije z označenimi lokacijami, ki vsebujejo podatke o **temperaturi** in **video kamerah**.

---

##  Glavne funkcionalnosti

- Prikaz Leaflet zemljevida z označenimi lokacijami iz baze
- Prikaz trenutne temperature na posameznih točkah (če obstaja)
- Prikaz povezav do kamer za opazovanje prometa/vremena
- Uporabniški sistem z registracijo, prijavo in JWT avtentikacijo
- Podatki o temperaturi in kamerah se pridobivajo iz baze (MySQL)
- Podpora za CORS in uporabo preko drugega strežnika (npr. na portu 8000)
- Samodejno generirana dokumentacija z uporabo `flask_selfdoc`

---


##  Namestitev

1. Kloniraj repozitorij:
```bash
git clone https://github.com/tvoje_uporabnisko_ime/ime-projekta.git
cd ime-projekta

2. Aktiviraj virtuelno okolje
python3 -m venv venv
source venv/bin/activate

3. namesti requirements
pip install -r requirements.txt

4. Ustvari .env datoteko z vsebino:
DB_HOST=localhost
DB_USER=uporabnik
DB_PASSWORD=geslo
DB_NAME=ime_baze
JWT_SECRET_KEY=skrivni_kljuc

5. zaženi aplikacijo:
python app.py

6. zaženi frontend lokalno:
cd static
python3 -m http.server 8000





