import tkinter as tk
import random

# Versuche winsound für den klassischen Error-Sound zu laden (nur Windows)
try:
    import winsound

    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

"""View: erstellt das Fenster im Windows 95/98 Style.
Stellt nur eine Callback-Registrierung und eine Update-Methode bereit.
Keine Logikänderungen durchgeführt.
"""


class PasswortSpielGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Eingabeaufforderung")
        self.root.geometry("350x120")

        # Windows 9x Hintergrundgrau
        self.bg_color = "#C0C0C0"
        self.root.configure(bg=self.bg_color)
        self.root.resizable(False, False)

        # UI-only state
        self.change_callback = None
        self.error_windows = {}  # Speichert {regel.beschreibung: Toplevel-Fenster}
        self.won = False

        self.create_widgets()

    def create_widgets(self):
        # Typischer Win9x Font
        font_win = ("MS Sans Serif", 9)

        tk.Label(
            self.root,
            text="Bitte geben Sie ein gültiges Passwort ein:",
            font=font_win,
            bg=self.bg_color
        ).pack(pady=(15, 5))

        self.password_var = tk.StringVar()
        self.password_var.trace_add("write", self._on_password_change)

        self.password_entry = tk.Entry(
            self.root,
            textvariable=self.password_var,
            font=font_win,
            width=40,
            relief="sunken",
            bd=2
        )
        self.password_entry.pack(pady=5)
        self.password_entry.focus()

        # Simple Statusleiste für das Level
        self.level_label = tk.Label(
            self.root,
            text="Level 1",
            font=font_win,
            bg=self.bg_color,
            relief="sunken",
            anchor="w",
            bd=1
        )
        self.level_label.pack(side="bottom", fill="x", padx=2, pady=2)

    def play_error_sound(self):
        """Spielt den klassischen Windows Error Sound ab."""
        if HAS_WINSOUND:
            # SystemHand = Critical Stop Sound
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC)
        else:
            self.root.bell()

    def spawn_error_window(self, beschreibung):
        """Erstellt ein nicht-schließbares Fehler-Fenster für eine unerfüllte Regel."""
        if beschreibung in self.error_windows:
            return  # Fenster existiert bereits für diese Regel

        err_win = tk.Toplevel(self.root)
        err_win.title("Schwerer Ausnahmefehler")
        err_win.configure(bg=self.bg_color)
        err_win.resizable(False, False)

        # Das Fenster als Werkzeugfenster markieren, um es vom Hauptfenster abzuheben
        err_win.attributes("-toolwindow", True)

        # Blockiert das Schließen über das 'X'
        err_win.protocol("WM_DELETE_WINDOW", lambda: self.play_error_sound())

        # Zufällige Position auf dem Bildschirm
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = random.randint(50, max(50, screen_w - 400))
        y = random.randint(50, max(50, screen_h - 200))
        err_win.geometry(f"350x130+{x}+{y}")

        frame = tk.Frame(err_win, bg=self.bg_color)
        frame.pack(expand=True, fill="both", padx=15, pady=15)

        # Standard Error Icon
        icon = tk.Label(frame, bitmap="error", bg=self.bg_color)
        icon.pack(side="left", padx=(0, 15), anchor="n")

        msg = tk.Label(
            frame,
            text=beschreibung,
            bg=self.bg_color,
            font=("MS Sans Serif", 9),
            wraplength=250,
            justify="left"
        )
        msg.pack(side="left", anchor="n")

        # Sinnloser OK-Button, der das Fenster nicht schließt, sondern nur piept
        btn_frame = tk.Frame(err_win, bg=self.bg_color)
        btn_frame.pack(side="bottom", pady=10)
        btn = tk.Button(
            btn_frame,
            text="OK",
            width=10,
            relief="raised",
            bd=2,
            bg=self.bg_color,
            command=self.play_error_sound
        )
        btn.pack()

        self.play_error_sound()
        self.error_windows[beschreibung] = err_win

    def close_error_window(self, beschreibung):
        """Schließt das Fenster, wenn die Regel erfüllt wurde."""
        if beschreibung in self.error_windows:
            self.error_windows[beschreibung].destroy()
            del self.error_windows[beschreibung]

    # --- Schnittstelle für den Controller ---
    def register_change_callback(self, callback):
        self.change_callback = callback

    def _on_password_change(self, *args):
        if self.change_callback is None or self.won:
            return
        passwort = self.password_var.get()
        try:
            self.change_callback(passwort)
        except Exception as e:
            print("Fehler im Change-Callback:", e)

    def update_from_controller(self, result: dict):
        if self.won:
            return

        aktive_regeln = result.get('aktive_regeln', [])
        regel_status = result.get('regel_status', [])
        level = result.get('level', 1)
        gewonnen = result.get('gewonnen', False)

        if gewonnen:
            self.won = True
            self.level_label.config(text="Vorgang erfolgreich beendet.")
            self.trigger_win_cascade()
            return

        self.level_label.config(text=f"Level {level}")

        aktuelle_beschreibungen = set()

        # Regeln prüfen und Fenster spawnen oder schließen
        for regel, ist_erfuellt in zip(aktive_regeln, regel_status):
            beschr = regel.beschreibung
            aktuelle_beschreibungen.add(beschr)
            if not ist_erfuellt:
                self.spawn_error_window(beschr)
            else:
                self.close_error_window(beschr)

        # Sicherheitshalber alte Fehler entfernen, falls Regeln komplett wegfallen
        for beschr in list(self.error_windows.keys()):
            if beschr not in aktuelle_beschreibungen:
                self.close_error_window(beschr)

    def trigger_win_cascade(self):
        """Spammt bei Sieg den Bildschirm mit Fehlern voll und crasht das Spiel."""
        self.password_entry.config(state="disabled")

        def spawn_random_error(count):
            if count > 0:
                addr = hex(random.randint(0x00000000, 0xFFFFFFFF)).upper()
                fake_beschr = f"Schwerer Ausnahme-Fehler 0E an {addr} in VxD VMM(01).\nDie aktuelle Anwendung wird beendet."
                self.spawn_error_window(fake_beschr)
                # Spawn das nächste Fenster in 150ms
                self.root.after(150, lambda: spawn_random_error(count - 1))
            else:
                # Schließt die gesamte Anwendung (alle Fenster)
                self.root.after(2000, self.root.destroy)

        # Spammt 30 Fehlerfenster
        spawn_random_error(30)


if __name__ == "__main__":
    app = PasswortSpielGUI()
    app.root.mainloop()