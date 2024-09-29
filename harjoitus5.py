import tkinter as tk
import threading
import time
import random
import winsound

root = tk.Tk()
root.title("Ernesti ja Kernesti - Autiolla saarella")

# Ikkunan koko
canvas_width = 800
canvas_height = 400

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Saaren ja mantereen piirtäminen
saari = canvas.create_rectangle(50, 100, 150, 300, fill="green", outline="black")
manner = canvas.create_rectangle(650, 100, 750, 300, fill="brown", outline="black")

# Meri
meri = canvas.create_rectangle(150, 100, 650, 300, fill="blue", outline="black")

# Hiekkaranta saareen
hiekka = canvas.create_rectangle(130, 100, 150, 300, fill="sandybrown", outline="black")

# E ja K visualisointi saarelle
ernesti = canvas.create_oval(60, 120, 90, 150, fill="yellow", outline="black")  # Ernesti on keltainen
kernesti = canvas.create_oval(60, 250, 90, 280, fill="red", outline="black")  # Kernesti on punainen

canvas.create_text(75, 110, text="Ernesti", font=("Arial", 10), fill="black")
canvas.create_text(75, 240, text="Kernesti", font=("Arial", 10), fill="black")

# Pohteri ja Eteteri visualisointi mantereelle
pohteri = canvas.create_oval(660, 120, 690, 150, fill="blue", outline="black")
eteteri = canvas.create_oval(660, 250, 690, 280, fill="green", outline="black")

canvas.create_text(675, 110, text="Pohteri", font=("Arial", 10), fill="black")
canvas.create_text(675, 240, text="Eteteri", font=("Arial", 10), fill="black")

# Hätäviesti yksittäisinä sanoina
alkuperaiset_sanat = [
    "Ernesti", "ja", "Kernesti", "tässä", "terve!",
    "Olemme", "autiolla", "saarella,", "voisiko", "joku",
    "tulla", "sieltä", "sivistyneestä", "maailmasta", "hakemaan",
    "meidät", "pois!", "Kiitos!"
]

ernesti_sanat = alkuperaiset_sanat.copy()
kernesti_sanat = alkuperaiset_sanat.copy()

# Apinan liikkeen "askelpituus"
step_size = 5

ernesti_saapuneet = set()
kernesti_saapuneet = set()

kilpailu_paattynyt = False
lock = threading.Lock()

def soita_kilometrin_aani(kilometri):
    if kilometri % 10 == 0:  # Soitetaan ääni vain 10 kilometrin välein, kone ei jaksa siltikään ääniä oikeaan aikaan :D
        winsound.Beep(1000, 300)

def soita_perille_aani(): # Ääni perillepääsyn merkiksi
    winsound.Beep(1500, 500)

def opeta_sana(sanalista):
    if not sanalista:
        sanalista.extend(alkuperaiset_sanat)  # opetetaan apinoille jatkuvalla syötöllä pelastusviestin sanoja järjestyksessä

    sana = sanalista.pop(0)
    print(f"Apinalle opetettiin sana: {sana}") # Printataan opetettu sana
    return sana

def evakuoi_voittaja(voittaja): # Voittajan evakuointi
    global kilpailu_paattynyt
    with lock:
        if kilpailu_paattynyt:
            return
        kilpailu_paattynyt = True

        laiva = canvas.create_rectangle(650, 200, 750, 230, fill="gray", outline="black") # Laivan visualisointi kun peli loppuu

        def liikuta_laiva():
            while True:
                laiva_pos = canvas.coords(laiva)
                if laiva_pos[0] <= 100:
                    if voittaja == "Ernesti":
                        canvas.create_text(75, 40, text="Evakuointilaiva pohjoiseen", font=("Arial", 10), fill="black")
                        print("Ernesti voitti kilpailun ja evakuointilaiva saapuu saarelle! Ernesti riemuitsee!")
                    elif voittaja == "Kernesti":
                        canvas.create_text(675, 40, text="Evakuointilaiva etelään", font=("Arial", 10), fill="black")
                        print("Kernesti voitti kilpailun ja evakuointilaiva saapuu saarelle! Kernesti riemuitsee!")
                    break

                # Laivan liike jotta menee oikeaan päähän saarta
                if voittaja == "Ernesti":
                    y_kulku = -1
                else:
                    y_kulku = 0.7

                canvas.move(laiva, -step_size, y_kulku)
                root.update()
                time.sleep(0.1)

        threading.Thread(target=liikuta_laiva).start()
        juhla_ateriat()


def juhla_ateriat():
    global ernesti_saapuneet, kernesti_saapuneet
    
    pohteri_apinat = len(ernesti_saapuneet)
    eteteri_apinat = len(kernesti_saapuneet)

    kaikki_perille = pohteri_apinat + eteteri_apinat

    # 1 perille päässyt apina = 4 ruokittavaa henkilöä
    pohteri_henkilot = pohteri_apinat * 4
    eteteri_henkilot = eteteri_apinat * 4
    
    # Mustapippurin määrä
    mustapippuri_yhteensa = kaikki_perille * 2

    print("\nJuhlavalmistelut:")
    print(f"Pohteri (Ernestin puoli):")
    print(f"  Apinoita perille: {pohteri_apinat}, Ruokittavia henkilöitä: {pohteri_henkilot}")
    
    print(f"Eteteri (Kernestin puoli):")
    print(f"  Apinoita perille: {eteteri_apinat}, Ruokittavia henkilöitä: {eteteri_henkilot}")
    
    print(f"Yhteensä perille päässeitä apinoita: {kaikki_perille} (Yhteensä {pohteri_henkilot + eteteri_henkilot} henkilöä ruokittavaksi)")
    print(f"\nYhteensä mustapippuria kuluu: {mustapippuri_yhteensa} tl")

    # Vertaillaan juhlien komeutta
    if pohteri_apinat > eteteri_apinat:
        print("\nPohteri oli juhlavampi! Siellä oli enemmän apinoita.")
    elif pohteri_apinat < eteteri_apinat:
        print("\nEteteri oli juhlavampi! Siellä oli enemmän apinoita.")
    else:
        print("\nJuhlat olivat yhtä suuria molemmissa päissä.")

def tarkkaile_apinaa_pohteri(sana):
    global ernesti_saapuneet
    if sana not in ernesti_saapuneet:
        ernesti_saapuneet.add(sana)
        print(f"Pohteri havaitsi uuden sanan Ernestiltä: {sana}. Yhteensä {len(ernesti_saapuneet)}/10 erilaista sanaa perillä.")
    if len(ernesti_saapuneet) >= 10:
        evakuoi_voittaja("Ernesti")

def tarkkaile_apinaa_eteteri(sana):
    global kernesti_saapuneet
    if sana not in kernesti_saapuneet:
        kernesti_saapuneet.add(sana)
        print(f"Eteteri havaitsi uuden sanan Kernestiltä: {sana}. Yhteensä {len(kernesti_saapuneet)}/10 erilaista sanaa perillä.")
    if len(kernesti_saapuneet) >= 10:
        evakuoi_voittaja("Kernesti")

syotyjen_apinoiden_maara = 0


def liikuta_apina(apina, sana, lahettaja):
    kilometri = 0
    
    while True:
        current_position = canvas.coords(apina)

        if current_position[0] + step_size >= 650:
            canvas.move(apina, 650 - current_position[0], 0)
            soita_perille_aani()
            print(f"Apina saapui perille sanalla: {sana}")
            canvas.delete(apina)

            if lahettaja == "Ernesti":
                tarkkaile_apinaa_pohteri(sana)
            elif lahettaja == "Kernesti":
                tarkkaile_apinaa_eteteri(sana)

            break
        else:
            # Tarkistus onko kilpailu päättynyt
            if kilpailu_paattynyt:
                canvas.delete(apina)  # Poistetaan kaikki apinat
                break

            # Apinan hukkumismahdollisuudet
            kilometri += 1
            if kilometri % 10 == 0:
                soita_kilometrin_aani(kilometri)

            if random.random() < 0.007:  # 0.7% mahdollisuus hukkua, koska demoamalla 1% oli liikaa ja vain noin 6/20 pääsi perille
                canvas.delete(apina)
                break

        canvas.move(apina, step_size, 0)
        root.update()
        time.sleep(0.1)

def opeta_apinoita_ernesti():
    while not kilpailu_paattynyt:
        sana = opeta_sana(ernesti_sanat)
        apina = canvas.create_oval(130, 120, 150, 140, fill="yellow", outline="black")
        threading.Thread(target=liikuta_apina, args=(apina, sana, "Ernesti")).start()
        time.sleep(2)  # Lähetetään apinat pienellä tauolla, etteivät mene päällekkäin

def opeta_apinoita_kernesti():
    while not kilpailu_paattynyt:
        sana = opeta_sana(kernesti_sanat)
        apina = canvas.create_oval(130, 250, 150, 270, fill="red", outline="black")
        threading.Thread(target=liikuta_apina, args=(apina, sana, "Kernesti")).start()
        time.sleep(2)  # Lähetetään apinat pienellä tauolla, etteivät mene päällekkäin


# Napit apinoiden lähettämiseen
ernesti_button = tk.Button(root, text="Ernesti lähettää apinoita", command=lambda: threading.Thread(target=opeta_apinoita_ernesti).start())
ernesti_button.pack(side=tk.LEFT)

kernesti_button = tk.Button(root, text="Kernesti lähettää apinoita", command=lambda: threading.Thread(target=opeta_apinoita_kernesti).start())
kernesti_button.pack(side=tk.RIGHT)

root.mainloop()
