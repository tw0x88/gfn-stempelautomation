# gfn-stempelautomation
Python- und Selenium-basiertes Tool zur Automatisierung der Stempelzeiten der gfn für Start und Ende.
Zeiterfassung startet morgens randomisiert zwischen 8:18 Uhr und 8:27 Uhr.
Zeiterfassung endet abends randomisiert zwischen 16:32 Uhr und 16:36 Uhr.

In der aktuellen Version ist das Programm dazu gedacht dauerhaft zu laufen und einem so die Arbeit immer abzunehmen.
Dazu kommt jetzt eine Benachrichtigung über den **Messengerdienst Telegram**, der sagt ob man erfolgreich Ein- bzw. Ausgestempelt ist.
Dies ist **OPTIONAL**.

# Disclaimer

> **Wichtiger Hinweis:**  
> Diese Software ist **nur eine Demo** und dient ausschließlich Demonstrationszwecken.  
> Sie darf **nicht** für rechtlich verbindliche oder produktive Zwecke eingesetzt werden.  
> Der Entwickler übernimmt keinerlei Haftung für Schäden oder Verluste, die aus der Nutzung dieser Software resultieren.

# Requirements

> Im Stammordner sollte die geckodriver.exe von Mozilla liegen.
> Der aktuellste Mozilla Firefox Webbrowser sollte ebenfalls bereits installiert sein.
>
> [Mozilla Geckodriver GitHub](https://github.com/mozilla/geckodriver/releases)
> [Mozilla Webbrowser](https://www.mozilla.org/de/firefox/new/)
>
> Das Programm läuft mit Selenium, einem Programm um Webbrowser bzw deren Userinteraktionen zu automatisieren.
>
> `pip install selenium`
>
> Der Telegram-Bot ist optional. ist aber sehr praktisch, da man mitbekommt was das Programm macht.
> Das Modul python-telegram-bot ist nur für den telegramIDcheker.py notwendig und kann danach wieder deinstalliert werden wenn gewünscht.
>
> `pip install python-telegram-bot`

# Telegram Bot Setup

> 1. Suche auf Telegram nach dem Telegram eigenen Service "BotFather".
> 2. Lege einen eigenen Bot an. /newbot
> 3. Hol dir den API Token.
> 4. Sende eine Nachricht an deinen Bot.
> 5. Im Repository liegt eine telegramIDcheker.py, führe sie aus um deine Telegram-ID auszulesen.

# Telegram Notification Beispiel

> ![Telegram Notification Beispiel](https://github.com/tw0x88/gfn-stempelautomation/blob/06d5c154dbfcd277ed5b8c0cf5b731943b3d46df/readme_images/telegram_bsp.jpg)
