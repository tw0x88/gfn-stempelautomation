# ezclokin.py
# Benötigte Pakete: selenium

# Info:
# zeitautomation.py lässt sich mit 2 Startparametern starten.
# zeitautomation.py 1 = Automatik, 2 = Manuell
# zeitautomation.py 1 1 = Homeoffice, 2 = Standort

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import random
import time
import sys
import os

# Konstanten
HOMEPAGE_GFN = r"https://lernplattform.gfn.de/login/index.php"
ZEITERFASSUNG_BEENDEN_LINK = r"https://lernplattform.gfn.de/?stoppen=1"

# Variablen
uhrzeit_starten_H = 8
uhrzeit_starten_M = random.randint(15, 24) # Uhr / Timerange zum einstempeln um Automation zu verschleiern.
uhrzeit_beenden_H = 16
uhrzeit_beenden_M = random.randint(35, 36) # Uhr / Timerange zum ausstempeln um Automation zu verschleiern.

# Funktionen
def pause(kategorie):
	# Zufalls-Dauer in Sekunden.
	if kategorie == 1: #Kurze Pausen
		warten = random.uniform(0.33, 1.23)

	elif kategorie == 2: #Mittlere Pausen
		warten = random.uniform(1.13, 3.48)

	elif kategorie == 3: #Lange Pausen
		warten = random.uniform(3.68, 4.68)

	time.sleep(warten)

def abfrage_userdaten():
	# Öffnet Automatisierbaren Firefox Browser.
	# Benötigt aktuelle Gekcodriver.exe von mozilla
	global email
	global pw

	try:
		if not os.path.exists("credentials.py"):
			print("Benutzerdaten müssen nur beim ersten Mal eingegeben werden.")
			email = input("Gib deine Emailadresse ein: ")
			pw = input("Gib das Passwort ein: ")
			print()

			with open("credentials.py", "w") as datei:
				datei.write('email = "' + email + '" \n')
				datei.write('pw = "' + pw + '"')

			print("Benutzerdaten erfolgreich in credentials.py gespeichert. [Achtung Klartext!]")
			pause(1)
			return True

		else:
			import credentials as cds

			email = cds.email
			pw = cds.pw
			return True

	except Exception as error:
		print("abfrage_userdaten Fehler!", error)
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

def abfrage_modus():
	# Automatik = 1
	# Manuell = 2
	modus = False

	try:
		if len(sys.argv) >= 2:
			startparameter = sys.argv[1]

			if startparameter == "1":
				modus = int(startparameter)

			elif startparameter == "2":
				modus = int(startparameter)

			else:
				print("Startparameter ungültig! Nur 1 oder 2")
				return False

		else:
			ask_modus = True
			while ask_modus == True:
				print("Automatischer oder manueller Modus?")
				modus_eingabe = input("Automatisch = 1 / Manuell = 2 / Programm beenden = e ")
				print()
				if modus_eingabe == "1":
					modus = int(modus_eingabe)
					ask_modus = False

				elif modus_eingabe == "2":
					modus = int(modus_eingabe)
					ask_modus = False

				elif modus_eingabe == "e":
					print("Durch User beendet.")
					return False

				else:
					print("Eingabe ungültig! Nur 1, 2 oder e möglich.")

		return modus

	except Exception as error:
		print("abfrage_modus Fehler!", error)
		return False

def abfrage_ort():
	# Homeoffice = 1
	# Standort = 2
	ort = False

	try:
		if len(sys.argv) >= 3:
			startparameter = sys.argv[2]

			if startparameter == "1":
				ort = int(startparameter)

			elif startparameter == "2":
				ort = int(startparameter)

			else:
				print("Startparameter ungültig! Nur 1 oder 2")
				return False

		else:
			ask_ort = True
			while ask_ort == True:
				print("Bist du im Homeoffice oder am Standort?")
				ort_eingabe = input("Homeoffice = 1 / Standort = 2 / Programm beenden = e. ")
				print()
				if ort_eingabe == "1":
					ort = int(ort_eingabe)
					ask_ort = False

				elif ort_eingabe == "2":
					ort = int(ort_eingabe)
					ask_ort = False

				elif ort_eingabe == "e":
					print("Durch User beendet.")
					return False

				else:
					print("Eingabe ungültig! Nur 1, 2 oder e möglich.")

		return ort

	except Exception as error:
		print("abfrage_ort Fehler!", error)
		return False

def zeiterfassung_starten():
	try:
		time.sleep(1)	
		#aufklappenZeitStempel = driver.find_element("css selector", ".drawer-toggler > button:nth-child(1)")  # Ich glaube das hier ist überflüssig mittlerweile.
		#aufklappenZeitStempel.click()
		#time.sleep(1)

		if "Startzeit" not in driver.page_source:
			ort = abfrage_ort()			
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

def warten_auf_uhrzeit(hour, minute):
	try:	
		warten = True
		while warten == True:
			os.system("cls")
			
			if int(time.strftime("%H")) >= hour: # Zeittimer volle Stunden
				if int(time.strftime("%M")) >= minute: # Zeittimer Minuten
					warten = False

				else:
					print("Warten bis " + str(hour) + ":" + str(minute) + " Uhr. Jetzt ist es:", time.strftime("%H:%M"), "Uhr")
					time.sleep(20) # Warte 20 Sekunden

			else:
				print("Warten bis " + str(hour) + ":" + str(minute) + " Uhr. Jetzt ist es:", time.strftime("%H:%M"), "Uhr")
				time.sleep(300) # Warte 5 Minuten

	except Exception as error:
		print("warten_auf_uhrzeit", error)

driver = None

try:
	os.system("cls") # Bereinigt die Terminalausgabe.
	if abfrage_userdaten() == True:
		modus = abfrage_modus()
		if modus == 1: # Automatik
			warten_auf_uhrzeit(uhrzeit_starten_H, uhrzeit_starten_M)
			if browser_und_login() == True:
				if zeiterfassung_starten() == True:
					driver.quit()

					warten_auf_uhrzeit(uhrzeit_beenden_H, uhrzeit_beenden_M)
					if browser_und_login() == True:
						pause(2)
						zeiterfassung_beenden()
						pause(2)

		elif modus == 2: # Manuell
			if browser_und_login() == True:
				ask_startenbeenden = True
				while ask_startenbeenden == True:
					print("Soll Zeiterfassung gestartet oder beendet werden?")
					startenbeenden = input("Schreibe 1 zum starten / 2 zum beenden / e um das Programm zu beenden. ")

					if startenbeenden == "1":
						if zeiterfassung_starten() == True:
							ask_startenbeenden = False

					elif startenbeenden == "2":
						zeiterfassung_beenden()
						ask_startenbeenden = False

					elif startenbeenden == "e":
						ask_startenbeenden = False
						print("Durch User beendet.")

					else:
						print("Falsche Eingabe!")

except Exception as error:
	print("Hauptstrang Fehler!", error)

finally:
	if driver:
		driver.quit()

	exit("Ende.")