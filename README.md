# Määährobot

@maehrobot ist ein [Telegram](https://telegram.org) bot, der Schafe (:sheep: und :ram:) automatisch mit einem herzlichen "määäh" grüsst.

Wenn du möchtest, kannst du das Schaf :sheep: auch etwas sagen lassen, versuche z.B. "/say Hi!".

## Mit dem Määährobot reden

Gehe auf [t.me/meahrobot](https://t.me/maehrobot) oder tippe eine Nachricht an `@maehrobot` direkt in Telegram.

## Selber hosten

Du musst den Määährobot nicht selber hosten, um mit ihm zu kommunizieren. Dazu musst du wirklich nur auf den Link oben klicken.

Falls du wirklich deine eigene Instanz vom Määährobot betreiben möchtest, sind folgende Schritte nötig:

* Klone dieses Repo: `git clone git@github.com:romanc/maehrobot.git maehrobot`
* Erstelle eine virtuelle [python](https://www.python.org) Umgebung: `python3 -m venv venv`
* Installiere die Abhängigkeiten `pip install -r requirements.txt` in die virtuelle Umgebung
* Kopiere `config.ini.example` zu `config.ini`, hole dir ein [Telegram bot token](https://core.telegram.org/bots#creating-a-new-bot) und konfiguriere den Token in die neu erstelle Konfigurationsdatei.
* Starte den bot mit `python maehrobot.py`
