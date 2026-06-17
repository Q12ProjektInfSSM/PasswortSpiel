import tkinter as tk
from tkinter import messagebox


"""View: erstellt das Fenster und stellt nur eine
Callback-Registrierung und eine Update-Methode für den Controller bereit.

Die Spiellogik ist vollständig im Model (`game.py`); der Controller
vermittelt zwischen View und Model.
"""


class PasswortSpielGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Das Passwort-Spiel")
        self.root.geometry("450x450")
        self.root.configure(bg="#f4f4f9")

        # UI-only state
        self.rules_labels = []
        self.change_callback = None  # vom Controller zu setzen

        self.create_widgets()

    def create_widgets(self):
        # Haupttitel
        tk.Label(self.root, text="🔒 Das Passwort-Spiel", font=("Arial", 16, "bold"), bg="#f4f4f9", fg="#333").pack(pady=15)
        # Level-Anzeige
        self.level_label = tk.Label(self.root, text="Level 1", font=("Arial", 12, "bold"), bg="#f4f4f9", fg="#555")
        self.level_label.pack(pady=5)

        # Label über dem Eingabefeld
        tk.Label(
            self.root,
            text="Gib dein Passwort ein:",
            font=("Arial", 10),
            bg="#f4f4f9"
        ).pack(pady=2)

        # Passwort-Variable mit Trace: informiert den Controller via registrierten Callback
        self.password_var = tk.StringVar()
        self.password_var.trace_add("write", self._on_password_change)

        # Das Eingabefeld (sichtbarer Text)
        self.password_entry = tk.Entry(
            self.root,
            textvariable=self.password_var,
            font=("Arial", 12),
            width=30
        )
        self.password_entry.pack(pady=10)
        self.password_entry.focus()

        # Kasten für die dynamische Regelübersicht
        self.rules_frame = tk.LabelFrame(
            self.root,
            text="Aktive Regeln",
            font=("Arial", 10, "bold"),
            bg="#f4f4f9",
            padx=15,
            pady=15
        )
        self.rules_frame.pack(pady=15, fill="both", expand=True, padx=25)

    # --- Schnittstelle für den Controller ---
    def register_change_callback(self, callback):
        """Controller ruft diese Methode, um über Passwort-Änderungen informiert zu werden.
        callback(passwort: str) wird bei jeder Änderung aufgerufen."""
        self.change_callback = callback

    def _on_password_change(self, *args):
        if self.change_callback is None:
            return
        passwort = self.password_var.get()
        try:
            # Controller wird informiert und erwartet die Passwort-Zeichenkette
            self.change_callback(passwort)
        except Exception as e:
            # Fehler im Controller dürfen die GUI nicht abstürzen lassen
            print("Fehler im Change-Callback:", e)

    def update_from_controller(self, result: dict):
        """Wird vom Controller aufgerufen. Erwartet ein Dict mit Schlüsseln:
        'aktive_regeln' (Liste von Regel-Objekten),
        'regel_status' (Liste von booleans),
        'level' (int),
        'gewonnen' (bool)
        Die View aktualisiert nur die Anzeige, keine Logik.
        """
        # Alte Regel-Labels löschen
        for lbl in self.rules_labels:
            lbl.destroy()
        self.rules_labels.clear()

        aktive_regeln = result.get('aktive_regeln', [])
        regel_status = result.get('regel_status', [])
        level = result.get('level', 1)
        gewonnen = result.get('gewonnen', False)

        # Level-Label
        if not gewonnen:
            self.level_label.config(text=f"Level {level}", fg="#555")
        else:
            self.level_label.config(text="🎉 Alle Level geschafft!", fg="#2e7d32")

        # Regeln anzeigen
        for regel, ist_erfuellt in zip(aktive_regeln, regel_status):
            icon = "✅" if ist_erfuellt else "❌"
            farbe = "#2e7d32" if ist_erfuellt else "#c62828"
            lbl = tk.Label(
                self.rules_frame,
                text=f"{icon} {regel.beschreibung}",
                font=("Arial", 11),
                fg=farbe,
                bg="#f4f4f9",
                anchor="w"
            )
            lbl.pack(fill="x", pady=3)
            self.rules_labels.append(lbl)

        # Wenn gewonnen: Eingabe sperren und Info anzeigen
        if gewonnen:
            self.password_entry.config(state="disabled")
            messagebox.showinfo("Gewonnen!", "🎉 Herzlichen Glückwunsch!\nDu hast das Spiel gewonnen!")


if __name__ == "__main__":
    app = PasswortSpielGUI()
    app.root.mainloop()
