import json
import os

def translate_manuscript(corpus_path="data/full_manuscript_transcription.txt", lexicon_path="data/fvsm_master_lexicon.json", output_path="outputs/full_manuscript_translation.txt"):
    if not os.path.exists(corpus_path) or not os.path.exists(lexicon_path):
        print("[ERROR] Corpus or lexicon file missing.")
        return

    with open(lexicon_path, 'r', encoding='utf-8') as f:
        lexicon_data = json.load(f)
        stems = lexicon_data.get("mapped_stems", {})

    translation_map = {}
    for token, details in stems.items():
        if isinstance(details, dict):
            defn = details.get("definition", token)
        else:
            defn = str(details)
        # Extract the primary short term for readability
        short_defn = defn.split('/')[0].strip().upper()
        translation_map[token.upper()] = short_defn

    translated_lines = []
    
    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("["):
                translated_lines.append(line)
                continue
            
            original_tokens = line.split()
            translated_tokens = []
            for t in original_tokens:
                # Strip punctuation for lookup, then apply translation
                stripped = "".join(c for c in t if c.isalnum()).upper()
                translated_defn = translation_map.get(stripped, stripped)
                translated_tokens.append(f"({translated_defn})")
            
            translated_lines.append(" ".join(translated_tokens) + "\n")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(translated_lines)

    print(f"\n[SUCCESS] Full manuscript decipherment saved to {output_path}")
    
    print("\n--- Preview of Deciphered Manuscript Text ---")
    preview_count = 0
    for line in translated_lines:
        if not line.startswith("[") and line.strip():
            print(line.strip())
            preview_count += 1
            if preview_count >= 5:
                break

if __name__ == "__main__":
    translate_manuscript()
