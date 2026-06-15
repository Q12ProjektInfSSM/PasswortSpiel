from controller.controller import PasswortGameController
from view.eingabefeld import PasswortSpielGUI


def main():
    """Startet das Passwort-Spiel mit View und Controller."""
    gui = PasswortSpielGUI()
    controller = PasswortGameController()
    controller.attach_view(gui)
    gui.root.mainloop()


if __name__ == "__main__":
    main()

