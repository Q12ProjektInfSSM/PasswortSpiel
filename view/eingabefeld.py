import tkinter as tk
import random
import threading
from playsound3 import playsound
"""View: erstellt das Fenster im Windows 95/98 Style.
Jede Regel erhält ein eigenes, dynamisches Popup-Fenster.
"""


class PasswortSpielGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Eingabeaufforderung")
        # Hauptfenster vergrößert für die massivere Textbox
        self.root.geometry("600x220")

        # Ein etwas weicheres, klassischeres Windows 98 Grau
        self.bg_color = "#D4D0C8"
        self.root.configure(bg=self.bg_color)
        self.root.resizable(False, False)

        # UI-only state
        self.change_callback = None
        self.rule_windows = {}  # Speichert {beschreibung: {"win": Toplevel, "lbl": Label, "ico": Label, "status": bool}}
        self.won = False

        self.create_widgets()

    def create_widgets(self):
        font_win = ("MS Sans Serif", 10)
        font_entry = ("MS Sans Serif", 16, "bold")  # Deutlich größere und fette Schrift für das Passwort

        # Ein innerer Rahmen (Frame) mit 3D-Effekt für die schönere Retro-Optik
        main_frame = tk.Frame(self.root, bg=self.bg_color, relief="ridge", bd=3)
        main_frame.pack(expand=True, fill="both", padx=12, pady=12)

        tk.Label(
            main_frame,
            text="Bitte geben Sie ein gültiges Passwort ein:",
            font=font_win,
            bg=self.bg_color
        ).pack(pady=(20, 10))

        self.password_var = tk.StringVar()
        self.password_var.trace_add("write", self._on_password_change)

        # Größere Textbox (Breite angepasst an die größere Schrift)
        self.password_entry = tk.Entry(
            main_frame,
            textvariable=self.password_var,
            font=font_entry,
            width=35,
            relief="sunken",
            bd=3
        )
        self.password_entry.pack(pady=10, padx=20)
        self.password_entry.focus()

        # Statusleiste für das Level
        self.level_label = tk.Label(
            self.root,
            text=" Level 1",
            font=("MS Sans Serif", 9),
            bg=self.bg_color,
            relief="sunken",
            anchor="w",
            bd=2
        )
        self.level_label.pack(side="bottom", fill="x", padx=2, pady=2)

    def play_error_sound(self):
        threading.Thread(
            target=playsound,
            args=("assets/erro.mp3",),
            daemon=True
        ).start()

    def manage_rule_window(self, beschreibung, ist_erfuellt):
        """Erstellt oder aktualisiert das separate Popup-Fenster für eine Regel."""
        farbe = "#008000" if ist_erfuellt else "#FF0000"
        titel = "Regel erfüllt" if ist_erfuellt else "Schwerer Ausnahmefehler"
        bitmap_type = "info" if ist_erfuellt else "error"
        symbol = "✔ " if ist_erfuellt else "❌ "

        # 1. Wenn das Fenster für die Regel noch nicht existiert -> Neu erstellen
        if beschreibung not in self.rule_windows:
            err_win = tk.Toplevel(self.root)
            err_win.configure(bg=self.bg_color)
            err_win.resizable(False, False)
            err_win.attributes("-toolwindow", True)

            # Blockiert das Schließen über das 'X'
            err_win.protocol("WM_DELETE_WINDOW", lambda: self.play_error_sound())

            # Zufällige Position auf dem Bildschirm
            screen_w = self.root.winfo_screenwidth()
            screen_h = self.root.winfo_screenheight()
            x = random.randint(50, max(50, screen_w - 400))
            y = random.randint(50, max(50, screen_h - 200))
            err_win.geometry(f"400x140+{x}+{y}")

            frame = tk.Frame(err_win, bg=self.bg_color)
            frame.pack(expand=True, fill="both", padx=15, pady=15)

            icon = tk.Label(frame, bg=self.bg_color)
            icon.pack(side="left", padx=(0, 15), anchor="n")

            msg = tk.Label(
                frame,
                bg=self.bg_color,
                font=("MS Sans Serif", 10),
                wraplength=280,
                justify="left"
            )
            msg.pack(side="left", anchor="n")

            # OK-Button (piept nur)
            btn_frame = tk.Frame(err_win, bg=self.bg_color)
            btn_frame.pack(side="bottom", pady=10)
            btn = tk.Button(
                btn_frame,
                text="OK",
                width=12,
                relief="raised",
                bd=2,
                bg=self.bg_color,
                command=self.play_error_sound
            )
            btn.pack()

            # Im State registrieren (status=None erzwingt gleich das farbliche Update)
            self.rule_windows[beschreibung] = {
                "win": err_win,
                "lbl": msg,
                "ico": icon,
                "status": None
            }

        # 2. Zustand des Fensters live anpassen, falls er sich geändert hat
        window_data = self.rule_windows[beschreibung]
        if window_data["status"] != ist_erfuellt:
            window_data["win"].title(titel)
            window_data["lbl"].config(text=f"{symbol}{beschreibung}", fg=farbe)
            window_data["ico"].config(bitmap=bitmap_type)
            window_data["status"] = ist_erfuellt

            # Sound nur abspielen, wenn die Regel (wieder) fehlschlägt
            if not ist_erfuellt:
                self.play_error_sound()

    def close_rule_window(self, beschreibung):
        """Schließt ein Fenster komplett (falls eine Regel aus dem Spiel fliegt)."""
        if beschreibung in self.rule_windows:
            self.rule_windows[beschreibung]["win"].destroy()
            del self.rule_windows[beschreibung]

    # --- Schnittstelle für den Controller ---
    def register_change_callback(self, callback):
        self.change_callback = callback

    def _on_password_change(self, *args):
        if self.change_callback is None or self.won:
            return
        passwort = self.password_var.get()

        # Dynamische Anpassung der Textfeld-Breite bei sehr langen Passwörtern
        neue_breite = max(35, len(passwort) + 5)
        self.password_entry.config(width=neue_breite)

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
            self.level_label.config(text=" Vorgang erfolgreich beendet.")
            # Bei Sieg alle echten Regel-Popups schließen vor der Kaskade
            for beschr in list(self.rule_windows.keys()):
                self.close_rule_window(beschr)
            self.trigger_win_cascade()
            return

        self.level_label.config(text=f" Level {level}")

        aktuelle_beschreibungen = set()

        # Jede aktive Regel verarbeiten (Popup öffnen oder updaten)
        for regel, ist_erfuellt in zip(aktive_regeln, regel_status):
            beschr = regel.beschreibung
            aktuelle_beschreibungen.add(beschr)
            self.manage_rule_window(beschr, ist_erfuellt)

        # Alte Fenster entfernen, falls Regeln komplett wegfallen
        for alte_beschr in list(self.rule_windows.keys()):
            if alte_beschr not in aktuelle_beschreibungen:
                self.close_rule_window(alte_beschr)

    def trigger_win_cascade(self):
        """Spammt bei Sieg den Bildschirm mit extrem vielen Fehlern voll und crasht das Spiel."""
        self.password_entry.config(state="disabled")

        def spawn_random_error(count):
            if count > 0:
                fake_beschr = f"DU GEWINNST!!!!a🥳🥳🎉🎉🪩🎊🪅"

                # Nutze die bestehende Logik für ein fehlerhaftes Popup
                err_win = tk.Toplevel(self.root)
                err_win.title("Schwerer Ausnahmefehler")
                err_win.configure(bg=self.bg_color)
                err_win.attributes("-toolwindow", True)

                screen_w = self.root.winfo_screenwidth()
                screen_h = self.root.winfo_screenheight()
                x = random.randint(10, max(10, screen_w - 400))
                y = random.randint(10, max(10, screen_h - 150))
                err_win.geometry(f"380x140+{x}+{y}")

                frame = tk.Frame(err_win, bg=self.bg_color)
                frame.pack(expand=True, fill="both", padx=15, pady=15)
                tk.Label(frame, bitmap="error", bg=self.bg_color).pack(side="left", padx=(0, 15))
                tk.Label(frame, text=fake_beschr, font=("MS Sans Serif", 9), bg=self.bg_color, justify="left").pack(side="left")

                # Viel schnellerer Spam (50ms statt 150ms)
                self.root.after(50, lambda: spawn_random_error(count - 1))
            else:
                self.root.after(3000, self.root.destroy)

        # Massiv erhöhte Anzahl an Fehlermeldungen für maximales Chaos (100 statt 30)
        spawn_random_error(100)
        threading.Thread(
            target=playsound,
            args=("assets/street-fighter-ii-you-win-perfect.mp3",),
            daemon=True
        ).start()