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
        return passwort[len(passwort)-1] == "©" or passwort[len(passwort)-1] == "™"

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
            "Deutschland": "Berlin",
            "Frankreich": "Paris",
            "Italien": "Rom",
            "Spanien": "Madrid",
            "Portugal": "Lissabon",
            "Österreich": "Wien",
            "Schweiz": "Bern",
            "Niederlande": "Amsterdam",
            "Belgien": "Brüssel",
            "Dänemark": "Kopenhagen",
            "Schweden": "Stockholm",
            "Norwegen": "Oslo",
            "Finnland": "Helsinki",
            "Polen": "Warschau",
            "Tschechien": "Prag",
            "Ungarn": "Budapest",
            "Griechenland": "Athen",
            "Türkei": "Ankara",
            "Japan": "Tokio",
            "China": "Peking",
            "Südkorea": "Seoul",
            "Indien": "Neu-Delhi",
            "Australien": "Canberra",
            "Kanada": "Ottawa",
            "USA": "Washington",
            "Mexiko": "Mexiko-Stadt",
            "Brasilien": "Brasília",
            "Argentinien": "Buenos Aires",
            "Ägypten": "Kairo",
            "Südafrika": "Pretoria"
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