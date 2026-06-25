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