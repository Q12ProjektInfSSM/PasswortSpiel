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
