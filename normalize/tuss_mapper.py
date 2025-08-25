import pandas as pd
from rapidfuzz import process, fuzz

class TussMapper:
    def __init__(self, csv_path: str):
        df = pd.read_csv(csv_path)  # colunas: code, name, synonyms(optional)
        self.index = {}
        for _, r in df.iterrows():
            names = [r["name"]] + (str(r.get("synonyms","")).split("|") if pd.notna(r.get("synonyms")) else [])
            for n in names:
                self.index[n.strip().lower()] = (r["code"], r["name"])

        self.keys = list(self.index.keys())

    def map_term(self, term: str) -> tuple[str, str, float]:
        cand, score, _ = process.extractOne(term.lower(), self.keys, scorer=fuzz.WRatio)
        code, name = self.index[cand]
        return code, name, score/100.0