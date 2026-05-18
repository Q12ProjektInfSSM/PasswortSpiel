class Regel:
def __init__(self, beschreibung):
self.beschreibung = beschreibung

def pruefen(self, passwort):
return True


class MindestlaengeRegel(Regel):
def __init__(self, min_laenge):
super().__init__(f"Mindestens {min_laenge} Zeichen")
self.min_laenge = min_laenge

def pruefen(self, passwort):
return len(passwort) >= self.min_laenge


class ZahlRegel(Regel):
def __init__(self):
super().__init__("Mindestens eine Zahl")

def pruefen(self, passwort):
return any(char.isdigit() for char in passwort)
