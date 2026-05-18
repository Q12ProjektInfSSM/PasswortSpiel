from model.regel import MindestlaengeRegel, ZahlRegel


class PasswortSpiel:
def __init__(self):
self.regeln = [
MindestlaengeRegel(5),
ZahlRegel()
]

def starten(self):

print("Willkommen beim Passwortspiel!")

while True:

passwort = input("Passwort eingeben: ")

alles_ok = True

for regel in self.regeln:

if not regel.pruefen(passwort):
print("Fehler:", regel.beschreibung)
alles_ok = False

if alles_ok:
print("Passwort korrekt!")
break
