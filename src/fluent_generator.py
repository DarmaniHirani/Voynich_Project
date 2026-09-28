import json
import os

def generate_fluent_text(translation_path="outputs/full_manuscript_translation.txt", output_path="outputs/fluent_manuscript_reading.txt"):
    if not os.path.exists(translation_path):
        print("[ERROR] Translation file missing. Run the base translation first.")
        return

    fluent_lines = []

    with open(translation_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("["):
                fluent_lines.append("\n" + line)
                continue
            
            # Clean and extract terms from the categorical tags
            tags = [t.strip("()").lower() for t in line.split() if t.startswith("(")]
            if not tags:
                continue

            # Apply experimental prose connectors based on contextual domains
            sentence_parts = []
            for i, tag in enumerate(tags):
                if "herbal" in tag or "plant" in tag or "root" in tag or "leaf" in tag:
                    connector = "the botanical component of" if i == 0 else "with"
                elif "vessel" in tag or "distill" in tag or "fluid" in tag:
                    connector = "process through" if i == 0 else "using"
                elif "solar" in tag or "astronomical" in tag or "degree" in tag:
                    connector = "under celestial alignment of" if i == 0 else "at"
                else:
                    connector = "and"

                sentence_parts.append(f"{connector} {tag}")

            fluent_sentence = " ".join(sentence_parts).capitalize() + "."
            fluent_lines.append(fluent_sentence + "\n")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(fluent_lines)

    print(f"\n[SUCCESS] Experimental fluent reading saved to {output_path}")
    
    print("\n--- Preview of Experimental Fluent Reading ---")
    preview_count = 0
    for line in fluent_lines:
        if not line.startswith("[") and line.strip():
            print(line.strip())
            preview_count += 1
            if preview_count >= 5:
                break

if __name__ == "__main__":
    generate_fluent_text()
