from telegram import Bot
import asyncio
import os

# Setze deinen Bot-Token
API_TOKEN = "###  Hier dein Telegram Bot API Token  ###"

async def main():
    bot = Bot(token=API_TOKEN)
    updates = await bot.get_updates()
    for update in updates:
        if update.message:
            user_id = update.message.from_user.id
            print(f"\tBenutzer-ID:  {user_id}")
            break

os.system("cls")

print("Sende spätestens jetzt eine Nachricht von deinem Ziel-Smartphone an deinen Bot.")
print()
input("Bestätige dass du soweit bist mit ENTER.")
print()
print()

asyncio.run(main())

print()
print()
print("Kopier dir die Zahlen der Benutzer-ID.")
print()
print("Falls es nicht geklappt hat. Stelle sicher das du schon eine Nachricht \nan deinen Bot gesendet hast und wiederhole die Schritte!")