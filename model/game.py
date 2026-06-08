
from model.regel import (
MindestLaengeRegel,
ZahlRegel,
GrossbuchstabeRegel,
SonderzeichenRegel
)


class PasswortSpiel:

def __init__(self):
self.regeln = [
MindestLaengeRegel(5),
ZahlRegel(),
GrossbuchstabeRegel(),
SonderzeichenRegel()
]

def starten(self):

print("=== Passwort-Spiel ===")

level = 1

while level <= len(self.regeln):

regel = self.regeln[level - 1]

print(f"\nLevel {level}")
print("Neue Regel:", regel.beschreibung)

passwort = input("Passwort eingeben: ")

erfolgreich = True

for i in range(level):
if not self.regeln[i].pruefen(passwort):
erfolgreich = False
print("❌ Regel nicht erfüllt:")
print("-", self.regeln[i].beschreibung)

if erfolgreich:
print("✅ Level geschafft!")
level += 1

print("\n🎉 Du hast das Spiel gewonnen!")
