"""Controller: vermittelt zwischen View und Model."""

from model.game import PasswortSpiel


class PasswortGameController:
    def __init__(self):
        # Model-Instanz
        self.game = PasswortSpiel()
        self.view = None

    def attach_view(self, view):
        self.view = view
        self.view.register_change_callback(self.on_password_changed)
        self.view.update_from_controller({
            "aktive_regeln": self.game.get_aktive_regeln(),
            "regel_status": [False for _ in self.game.get_aktive_regeln()],
            "level": self.game.level,
            "gewonnen": self.game.spiel_beendet,
        })

    def on_password_changed(self, passwort):
        result = self.game.analysiere_passwort(passwort)

        if self.view:
            self.view.update_from_controller({
                "aktive_regeln": result["aktive_regeln"],
                "regel_status": result["regel_status"],
                "level": result["level"],
                "gewonnen": result["gewonnen"],
            })


if __name__ == "__main__":
    # kleines Demo-Setup: Controller und View verbinden
    from view.eingabefeld import PasswortSpielGUI

    ui = PasswortSpielGUI()
    ctrl = PasswortGameController()
    ctrl.attach_view(ui)
    ui.root.mainloop()

