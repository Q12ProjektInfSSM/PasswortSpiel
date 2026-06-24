from model.regel import Regel
import requests


class FussballRegel(Regel):
    def get_score(self):
        API_KEY = "fd19bb98bff7434489c7f7a9d6d467e1"

        headers = {
            "X-Auth-Token": API_KEY
        }

        GERMANY_ID = 759

        url = f"https://api.football-data.org/v4/teams/{GERMANY_ID}/matches"

        params = {
            "status": "FINISHED",
            "limit": 1
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            last_match = data["matches"][0]

            home = last_match["homeTeam"]["name"]
            away = last_match["awayTeam"]["name"]

            home_score = last_match["score"]["fullTime"]["home"]
            away_score = last_match["score"]["fullTime"]["away"]

            if home == "Germany":
                self.result = f"{home_score}:{away_score}"
                self.opp = away
            else:
                self.result = f"{away_score}:{home_score}"
                self.opp = home

        except Exception:
            # Fallback, damit das Spiel trotzdem startet
            self.result = "0:0"
            self.opp = "unbekannt"

    def __init__(self):
        self.result, self.opp = "", ""
        self.get_score()
        super().__init__(
            f"Muss Ergebnis des letzten Deutschland-Spiels enthalten (TIPP: gegen {self.opp})"
        )

    def pruefen(self, passwort):
        return self.result in passwort