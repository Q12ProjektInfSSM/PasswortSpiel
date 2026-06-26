import periodictable as pt
class Regel:
    def __init__(self, beschreibung):
        self.beschreibung = beschreibung

    def pruefen(self, passwort):
        raise NotImplemented


class MindestLaengeRegel(Regel):

    def __init__(self, laenge):
        super().__init__(f"Mindestens {laenge} Zeichen")
        self.laenge = laenge

    def pruefen(self, passwort):
        return len(passwort) >= self.laenge


class ZahlRegel(Regel):
    def __init__(self):
        super().__init__("Mindestens eine Zahl")

    def pruefen(self, passwort):
        return any(c.isdigit() for c in passwort)


class GrossbuchstabeRegel(Regel):
    def __init__(self):
        super().__init__("Mindestens ein Großbuchstabe")

    def pruefen(self, passwort):
        return any(c.isupper() for c in passwort)


class SonderzeichenRegel(Regel):
    def __init__(self):
        super().__init__("Mindestens ein Sonderzeichen")

    def pruefen(self, passwort):
        sonderzeichen = "!@#$%^&*()-_=+[]{};:,<.>/?"
        return any(c in sonderzeichen for c in passwort)

class Copyright(Regel):
    def __init__(self):
        super().__init__("Soll Copyright-Geschützt sein ©")

    def pruefen(self, passwort):
        return passwort.endswith(("©", "™"))

class GeradeLaengeRegel(Regel):
    def __init__(self):
        super().__init__("Die Passwortlänge muss gerade sein")

    def pruefen(self, passwort):
        return len(passwort) % 2 == 0

class KeinERegel(Regel):
    def __init__(self):
        (super().__init__("Der Buchstabe 'e' darf nicht vorkommen"))

    def pruefen(self, passwort):
        return "e" not in passwort.lower()

class MorseSOSRegel(Regel):
    def __init__(self):
        super().__init__("Das Passwort muss 'SOS' als Morsecode enthalten")

    def pruefen(self, passwort):
        return "...---..." in passwort

class PalindromRegel(Regel):
    def __init__(self):
        super().__init__("Das Passwort muss ein Palindrom enthalten")

    def pruefen(self, passwort):
        woerter = passwort.split()

        for wort in woerter:
            if len(wort) > 1 and wort.lower() == wort.lower()[::-1]:
                return True

        return False

class PiRegel(Regel):
        def __init__(self):
            super().__init__("Das Passwort muss Pi enthalten")

        def pruefen(self, passwort):
            return "14159" in passwort or "3.14159" in passwort

class Summe30Regel(Regel):
    def __init__(self):
        super().__init__("Alle Ziffern im Passwort müssen summiert 40 ergeben")

    def pruefen(self, passwort):
        ziffern = [int(c) for c in passwort if c.isdigit()]
        return sum(ziffern) == 40
import random

class HauptstadtRegel(Regel):
    def __init__(self):
        self.orte = {
    "Frankreich": "Paris",
    "Italien": "Rom",
    "Spanien": "Madrid",
    "Portugal": "Lissabon",
    "Norwegen": "Oslo",
    "Polen": "Warschau",
    "Tschechien": "Prag",
    "Türkei": "Ankara",
    "Japan": "Tokio",
    "Kanada": "Ottawa",
    "USA": "Washington",
    "Brasilien": "Brasilia",
    "Ägypten": "Kairo"
}
        self.land, self.hauptstadt = random.choice(list(self.orte.items()))

        super().__init__(
            f"Das Passwort muss die Hauptstadt von {self.land} enthalten"
        )

    def pruefen(self, passwort):
        return self.hauptstadt.lower() in passwort.lower()

class KunstlehrerRegel(Regel):
    def __init__(self):
        super().__init__("Das Passwort muss den Namen eines Kunstlehrers enthalten")

        self.lehrer = ["krejci", "ernst", "fritz"]

    def pruefen(self, passwort):
        passwort = passwort.lower()
        return any(name in passwort for name in self.lehrer)


class ElementSummeRegel(Regel):
    def __init__(self):
        self.zielsumme = 180
        super().__init__(
            f"Die Summe der Ordnungszahlen aller chemischen Elemente muss {self.zielsumme} ergeben"
        )

        self.elemente = {
            e.symbol: e.number
            for e in pt.elements
            if e.number
        }

    def pruefen(self, passwort):
        summe = 0
        i = 0

        while i < len(passwort):
            if i + 1 < len(passwort):
                symbol = passwort[i:i+2]
                if symbol in self.elemente:
                    summe += self.elemente[symbol]
                    i += 2
                    continue

            symbol = passwort[i]
            if symbol in self.elemente:
                summe += self.elemente[symbol]

            i += 1
        self.beschreibung = f"Die Summe der Ordnungszahlen aller chemischen Elemente muss {self.zielsumme} ergeben. Aktuell: {summe}"

        return summe == self.zielsumme

class SchachfigurRegel(Regel):
    def __init__(self):
        super().__init__("Das Passwort muss eine Schachfigur enthalten")

    def pruefen(self, passwort):
        schachfiguren = "♔♕♖♗♘♙♚♛♜♝♞♟"
        return any(c in schachfiguren for c in passwort)