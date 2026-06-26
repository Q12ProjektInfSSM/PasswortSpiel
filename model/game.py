from model import jumpnrun
from model.jumpnrun import JumpnRunGame
from model.regel import (
    GrossbuchstabeRegel,
    MindestLaengeRegel,
    SonderzeichenRegel,
    ZahlRegel,
    Copyright,
    GameRegel,
    GeradeLaengeRegel,
    KeinERegel,
    MorseSOSRegel,
    PiRegel,
    Summe30Regel,
    HauptstadtRegel,
    KunstlehrerRegel,
    ElementSummeRegel,
    EmojiRegel
)
from model.fussball_regel import FussballRegel


class PasswortSpiel:
    """Passwort-Spiel mit schrittweiser Freischaltung der Regeln."""

    alle_regeln = [
        MindestLaengeRegel(5),
        ZahlRegel(),
        GrossbuchstabeRegel(),
        GameRegel(jumpnrun),
        SonderzeichenRegel(),
        Copyright(),
        FussballRegel(),
        MorseSOSRegel(),
        PiRegel(),
        Summe30Regel(),
        HauptstadtRegel(),
        KunstlehrerRegel(),
        KeinERegel(),
        GeradeLaengeRegel(),
        ElementSummeRegel(),
        EmojiRegel(),
    ]

    def __init__(self):
        self.regeln = list(PasswortSpiel.alle_regeln)
        self.level = 1
        self.spiel_beendet = False

    def reset(self):
        self.level = 1
        self.spiel_beendet = False

    def get_aktive_regeln(self):
        return self.regeln[: min(self.level, len(self.regeln))]

    def get_regel_status(self, passwort):
        return [regel.pruefen(passwort) for regel in self.get_aktive_regeln()]

    def _alle_sichtbaren_regeln_erfuellt(self, passwort):
        return all(regel.pruefen(passwort) for regel in self.get_aktive_regeln())

    def analysiere_passwort(self, passwort):
        """Prüft das Passwort und schaltet die nächste Regel frei, wenn alle sichtbaren erfüllt sind."""
        if not self.spiel_beendet:
            while self.level <= len(self.regeln) and self._alle_sichtbaren_regeln_erfuellt(passwort):
                if self.level == len(self.regeln):
                    self.spiel_beendet = True
                    break
                self.level += 1

        aktive_regeln = self.get_aktive_regeln()
        regel_status = [regel.pruefen(passwort) for regel in aktive_regeln]

        return {
            "aktive_regeln": aktive_regeln,
            "regel_status": regel_status,
            "level": self.level,
            "gewonnen": self.spiel_beendet,
        }