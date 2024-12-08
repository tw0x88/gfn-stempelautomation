from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from telegram import Bot
import asyncio
import random
import time
import os

# Konstanten
HOMEPAGE_GFN = "https://lernplattform.gfn.de/login/index.php"
ZEITERFASSUNG_BEENDEN_LINK = "https://lernplattform.gfn.de/?stoppen=1"

# Variablen
uhrzeit_starten_H = 8 # Stunde Einstempeln
uhrzeit_starten_M = random.randint(18, 27) # Timerange zum einstempeln um Automation zu verschleiern.
uhrzeit_beenden_H = 16 # Stunde Ausstempeln
uhrzeit_beenden_M = random.randint(32, 36) # Timerange zum ausstempeln um Automation zu verschleiern.

driver = None
bot = None

# Funktionen
def pause(kategorie):
	# Zufalls-Dauer in Sekunden.
	if kategorie == 1: #Kurze Pausen
		warten = random.uniform(0.33, 1.23)

	elif kategorie == 2: #Mittlere Pausen
		warten = random.uniform(1.13, 3.48)

	elif kategorie == 3: #Lange Pausen
		warten = random.uniform(3.68, 3.98)

	time.sleep(warten)

async def send_telegram_message(empfaenger_ID, message):
    try:
        await bot.send_message(chat_id = empfaenger_ID, text = message)
        print("Telegram-Message versandt.")

    except Exception as error:
        print(f"Fehler: {error}")

def abfrage_userdaten():
	global email
	global pw
	global ort
	global telegram_api_token
	global telegram_ID

	try:
		if not os.path.exists("credentials.py"):
			print("Benutzerdaten müssen nur beim ersten Mal eingegeben werden.")
			print()
			email = input("Gib deine Emailadresse ein: ")
			pw = input("Gib das Passwort ein: ")
			print()
			print("Homeoffice = 1 / Standort = 2")
			ort = int(input("Gib den Ort als Zahl ein: "))
			print()
			print("Um Benachrichtigungen unterwegs zu erhalten ob der Login erfolgreich durchgeführt wurde.")
			print("Solle das nicht gewünscht sein einfach leer lassen und Enter drücken.")
			telegram_api_token = input("Gib das Telegram API Token ein: ")
			print()
			print("Deine Telegram ID kannst du auch leer lassen wenn du keine Benachrichtigungen wünschst.")
			telegram_ID = int(input("Gib deine Telegram-ID ein: "))
			print()

			with open("credentials.py", "w") as datei:
				datei.write('email = "' + email + '" \n')
				datei.write('pw = "' + pw + '" \n')
				datei.write('ort = "' + str(ort) + '" \n')
				datei.write('tat = "' + telegram_api_token + '" \n')
				datei.write('tid = "' + str(telegram_ID + '"'))

			print("Benutzerdaten erfolgreich in credentials.py gespeichert. [Achtung Klartext!]")
			print()
			print("Solltest du deinen Ort mal verändern wollen, lösche einfach die credentials.py \noder änder die Zahl für den Ort darin entsprechend.")
			input("Weiter mit Enter!")
			return True

		else:
			import credentials as cds

			email = cds.email
			pw = cds.pw
			ort = int(cds.ort)
			telegram_api_token = int(cds.tat)
			telegram_ID = int(cds.tid)

			return True

	except Exception as error:
		print("abfrage_userdaten Fehler!", error)
		return False

def telegram_bot():
	global bot
	bot = Bot(token = telegram_api_token)

def browser_und_login():
	global driver

	try:
		optionen = Options()
		optionen.headless = False # False = Browser wird angezeigt

		print("Starte Firefox.")
		driver = webdriver.Firefox(options = optionen) # Starte Firefox
		driver.set_window_position(60, 60)
		driver.set_window_size(1500, 1100) # bxh

		print("Gehe zu:", HOMEPAGE_GFN)
		driver.get(HOMEPAGE_GFN) # Öffne GFN Lernplattform
		pause(3)

		print("Automatischer Login.")
		login_user_feld = driver.find_element("id", "username")
		login_password_feld = driver.find_element("id", "password")

		login_user_feld.send_keys(email)
		pause(1)
		login_password_feld.send_keys(pw)
		pause(1)
		login_password_feld.send_keys(Keys.RETURN)
		pause(3)

		if popup_handle() == True:
			if "Zeiterfassung Status" in driver.page_source:
				print("Einloggen erfolgreich.")

				if "Heute kein Unterricht!" in driver.page_source:
					print("Es findet heute anscheinend kein Unterricht statt.")
					return False

				else:
					return True

			else:
				return False

		else:
			return False
		
	except Exception as error:
		print("browser_und_login Fehler!", error)
		return False

def popup_handle():
	try: # Versuche zum alert zu switchen ohne zu wissen ob es da ist.
		pause(1)
		alert = driver.switch_to.alert
		alert.accept()
		print("Popup war da.")
		pause(1)
		return True

	except Exception as error: # Wenn es nicht da ist. Um so besser!
		print("Popup nicht da.")
		return True

def zeiterfassung_starten():
	try:
		time.sleep(1)
		stempler_rausholen = driver.find_element("css selector", "#topofscroll > div.drawer-toggles.d-flex > div > button")
		stempler_rausholen.click()
		time.sleep(0.3)

		if "Startzeit" not in driver.page_source:
			if ort == 1:
				zeit_radio_homeoffice = driver.find_element("css selector", "#flexRadioDefault1")
				zeit_radio_homeoffice.click()                                
				pause(2)
				ask_location = False

			elif ort == 2:
				zeit_radio_standort = driver.find_element("css selector", "#flexRadioDefault2")
				zeit_radio_standort.click()
				pause(2)
				ask_location = False

			else:
				return False

			zeit_submit_button = driver.find_element("css selector", "input[type='submit']")
			zeit_submit_button.click()

			pause(3)
			return True

		else:
			print("Die Zeiterfassung ist bereits gestartet worden.")

	except Exception as error:
		print("zeiterfassung_starten Fehler!", error)
		return False

def zeiterfassung_beenden():
	try:
		if "Endzeit" not in driver.page_source:
			driver.get(ZEITERFASSUNG_BEENDEN_LINK) # Ruft den Link zum Stoppen der Zeiterfassung auf.
			pause(3)

		else:
			print("Du bist bereits abgemeldet!")

	except Exception as error:
		print("zeiterfassung_beenden Fehler!", error)

# Funktion startet die Zeiterfasssung nur innerhalb eines Zeitfenster von 10 Minuten am Tag.
# So kann man sorglos später am Tag seinen Pc starten ohne das er Sich in die Zeit einstempelt.
def warten_auf_uhrzeit(hour, minute):
    try:	
        warten = True
        while warten == True:
            os.system("cls")

            strfHour = int(time.strftime("%H"))
            strfMinute = int(time.strftime("%M"))
            
            if strfHour == hour:
                if strfMinute >= minute and strfMinute <= minute + 10: # Zeitfenster 10 Minuten nach eingestellter Minute falls man den Pc zu spät startet.
                    warten = False

                else:
                    print("Warten bis " + str(hour) + ":" + str(minute) + " Uhr. Jetzt ist es: " + str(strfHour) + ":" + str(strfMinute) + " Uhr")
                    time.sleep(20) # Warte 20 Sekunden

            else:
                print("Warten bis " + str(hour) + ":" + str(minute) + " Uhr. Jetzt ist es: " + str(strfHour) + ":" + str(strfMinute) + " Uhr")
                time.sleep(300) # Warte 5 Minuten (300Sek)

    except Exception as error:
        print("warten_auf_uhrzeit", error)

try:
	os.system("cls") # Bereinigt die Terminalausgabe.
	if abfrage_userdaten() == True:
		warten_auf_uhrzeit(uhrzeit_starten_H, uhrzeit_starten_M)
		if browser_und_login() == True:
			if zeiterfassung_starten() == True:
				driver.quit()

				warten_auf_uhrzeit(uhrzeit_beenden_H, uhrzeit_beenden_M)
				if browser_und_login() == True:
					pause(2)
					zeiterfassung_beenden()
					pause(2)

except Exception as error:
	print("Programm Fehler!", error)

finally:
	if driver:
		driver.quit()

	exit("Ende.")