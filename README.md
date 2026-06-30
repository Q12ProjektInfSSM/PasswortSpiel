# Projektdokumentation: Das Passwort-Spiel (Code-Challenge)

## Einleitung und Spielidee
* Inspiration für dieses Spiel ist das Passwort-Spiel von neal.fun. Unsere Version sollte eigene lustige Regeln beinhalten, die eine schnelle Herausforderung bilden.
* **Spielprinzip & Ziel:** Der Spieler soll ein Passwort finden, dass allen verschiedenen Regeln entspricht, dabei steigt die Schwierigkeit jede Regel
* **Benutzerinteraktion:** Eingabe des Passworts erfolgt durch ein kleines Fenster mit Eingabezeile. nicht erfüllte Regeln ploppen in einem weiteren Fenster auf.

---

## Aufbau
Das Projekt ist ein Python-Projekt, der in mehrere Ordner/Module unterteilt sind, um der MVC-Architektur treu zu bleiben

- Model: beinhält die Logik des Spiels, in regel.py bzw. fussball_regel.py befinden sich die definierten regeln, die das Passwort erfüllen soll. in game.py befindet sich die Logik, um den aktuellen Spielstand zu speichern, und ein eingegebenes Passwort zu bewerten.
- View: beinhält eingabefeld.py. Die Funktion davon ist es. das Eingabefeld zu erstellen und Fenster für Fehler zu erstellen, außerdem ist die Siegesanimation darin vorhanden.
- Controller: controller.py regelt die Kommunikation zwischen der View und Model, indem beide Module erstellt werden, anschließend wird das Passwort von der Eingabe zum Model weitereleitet, das Ergebnis davon wird wieder an die GUI zur Anzeige versendet
- Assets: beinhält die Tondateien für das Aufploppen eines Fehlers oder das Gewinnen
- main.py startet das Spiel


---

## Dependencies
- tkinter: erstellt alle Fenster und Eingabefelder
- playsound: stellt methoden bereit, um Töne abzuspielen 
- random: Standard python-Bibliothek für Zufall
- requests: benötigt um api-calls zu machen
- periodictable: ermöglicht das Erstellen eines Dict mit Elementsymbol und Ordnungszahl

---

## Teamarbeit und Versionsverwaltung

- Aufteilung der Arbeit:
	- Sabri: (Spielidee mit Entwurf von Regeln, Spieltesten)
	- Stefan: (Umsetzung der Regeln & Projektstruktur)
	- Matthieu: (GUI, Projektstruktur, Regeln)

Verwaltung von GitHub zum zentralen Speichern des Projekts. Eigene Änderungen werden gemacht, anschließend mit der Repo gemergt 

---

## Ablauf

1. Spielidee finden, eigene Regeln ausdenken
2. Architektur und Projektstruktur bestimmen
3. Regeln implementieren + testen
4. Spiellogik mit Regelprüfung
5. GUI mit Contoller erstellen
