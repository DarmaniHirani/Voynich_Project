import json
import os

class BotanicalNomenclatureMapper:
    def __init__(self, lexicon_path):
        self.lexicon_path = lexicon_path
        self.lexicon = self._load_lexicon()
        
        self.species_database = {
            "root_stem_apothecary": {
                "cth": {"species": "Artemisia absinthium", "common": "Wormwood", "section": "Herbal"},
                "keod": {"species": "Mandragora officinarum", "common": "Mandrake", "section": "Herbal"},
                "ched": {"species": "Papaver somniferum", "common": "Opium Poppy", "section": "Herbal"},
                "sol": {"species": "Helianthus/Solar aligned", "common": "Stellar/Solar Herb", "section": "Astronomical"},
                "aloe": {"species": "Aloe vera", "common": "Aloe", "section": "Herbal"},
                "ros": {"species": "Rosmarinus officinalis", "common": "Rosemary", "section": "Herbal"},
                "lil": {"species": "Lilium candidum", "common": "White Lily", "section": "Herbal"},
                "cann": {"species": "Cannabis sativa", "common": "Hemp", "section": "Herbal"}
            }
        }

    def _load_lexicon(self):
        if os.path.exists(self.lexicon_path):
            with open(self.lexicon_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def map_token_to_species(self, token_stem):
        database = self.species_database.get("root_stem_apothecary", {})
        if token_stem in database:
            match = database[token_stem]
            return f"[MATCH] Stem '{token_stem}' identified as {match['species']} ({match['common']}) [{match['section']}]"
        return f"[UNMAPPED] Stem '{token_stem}' requires further historical iconography cross-reference."

if __name__ == "__main__":
    mapper = BotanicalNomenclatureMapper("data/fvsm_master_lexicon.json")
    test_stems = ["cth", "keod", "ched", "aloe", "ros", "unknown_stem"]
    
    print("--- Expanded Botanical Species Nomenclature Mapping Audit ---")
    for stem in test_stems:
        print(mapper.map_token_to_species(stem))
