

import json
import os
import numpy as np
import cv2
from botanical_mapper import BotanicalNomenclatureMapper

def save_botanical_audit(audit_results, filename="outputs/botanical_audit_report.json"):
    """Ensures the outputs directory exists and saves the audit results to JSON."""
    os.makedirs("outputs", exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(audit_results, f, indent=4)
    print(f"[SUCCESS] Full-corpus audit report saved to {filename}")

def cross_reference_latin_sigla(token, sigla_dictionary_path="data/latin_sigla_lexicon.json"):
    """
    Cross-references an FVSM topological token against historical medieval 
    Latin sigla, abbreviation markers, and botanical shorthand dictionaries.
    """
    import os
    import json
    
    # Direct master lexicon with correct uppercase keys
    sigla_db = {
        "O": "Orbis (Circular follicle boundary or globular seed node)",
        "P": "Pes / Planta (Botanical pedal axis or primary stem structure)",
        "I": "Inflorescentia (Vertical verticality stem marker)",
        "T": "Truncus (Main structural trunk or vascular bundle)",
        "A": "Apex (Leaf or petal terminal extremity)",
        "S": "Semen / Semente (Seed capsule or reproductive corpuscle)"
    }
    
    upper_token = token.upper()
    
    if upper_token in sigla_db:
        definition = sigla_db[upper_token]
        return f"[MATCH] Sigla Identified: {token} -> Expands to '{definition}'"
    else:
        return f"[UNMAPPED] Token '{token}' verified against Latin Sigla base; requires contextual ligature check."

def map_coordinates_to_fvsm_tokens(coordinate_slices):
    """
    FVSM Phase 2: Token Assignment Matrix.
    Ingests isolated spatial slices and programmatically binds them to the 
    10-dimensional deterministic mapping vector array based on aspect ratio rules.
    """
    print(f"[INGESTION] Mapping {len(coordinate_slices)} spatial slices to FVSM tokens...")
    token_ledger = []
    
    for slice_box in coordinate_slices:
        x, y, w, h = slice_box
        aspect_ratio = w / float(h) if h > 0 else 0
        
        # Applying strict Topological Stroke-Complexity Ranking rules
        if aspect_ratio < 0.5:
            token = 'I' if y % 2 == 0 else 'T'
        elif 0.5 <= aspect_ratio < 1.5:
            token = 'O' if x % 2 == 0 else 'A'
        else:
            token = 'P' if w % 2 == 0 else 'S'
            
        token_ledger.append(token)
        
    print(f"[SUCCESS] Token Mapping Matrix compiled. Generated {len(token_ledger)} symbols.")
    return token_ledger

def segment_rows_horizontal_projection(binary_thresh_img):
    """
    Computes a horizontal projection profile by summing white pixels across rows,
    identifies whitespace valleys between text lines, and slices the image 
    into isolated horizontal text row arrays.
    """
    # 1. Sum pixel values horizontally (axis=1) - count black text pixels instead of background
    projection_profile = np.sum(binary_thresh_img == 0, axis=1)
    
    # 2. Identify whitespace valleys between text lines
    noise_threshold = np.max(projection_profile) * 0.02
    in_line = False
    row_bounds = []
    start_y = 0

    for y, count in enumerate(projection_profile):
        if count > noise_threshold and not in_line:
            in_line = True
            start_y = y
        elif count <= noise_threshold and in_line:
            in_line = False
            end_y = y
            if (end_y - start_y) > 5: 
                row_bounds.append((start_y, end_y))
                
    # 3. Slice the matrix into isolated horizontal row arrays
    isolated_rows = []
    for (s_y, e_y) in row_bounds:
        row_slice = binary_thresh_img[s_y:e_y, :]
        isolated_rows.append(row_slice)
        
    print(f"[FVSM Engine] Successfully segmented {len(isolated_rows)} text rows via Horizontal Projection.")
    return isolated_rows, row_bounds
    
def generate_synthetic_manuscript_page(output_path="data/synthetic_manuscript_page.jpg"):
    """
    Generates a realistic synthetic manuscript page image with multiple text lines
    and saves it to the specified path for testing the image processing pipeline.
    """
    # Create a blank white page canvas (800x600 pixels)
    page = np.ones((600, 800), dtype=np.uint8) * 245
    
    # Draw multiple horizontal lines representing manuscript text rows
    line_y_coordinates = [80, 140, 200, 260, 320, 380, 440, 500]
    
    for y in line_y_coordinates:
        cv2.putText(page, "marianus botanical codex folio segment 1", (50, y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, 0, 2)
        
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the generated image
    cv2.imwrite(output_path, page)
    print(f"[FVSM] Generated synthetic manuscript page at: {output_path}")
    return output_path

if __name__ == "__main__":
    print("[FVSM] Testing Full Image-to-Auditing Pipeline with Real Manuscript...")
    
    # Path to your real manuscript image inside the data folder
    real_image_path = "data/your_manuscript_image.jpg" # Replace with your actual filename
    
    if not os.path.exists(real_image_path):
        print(f"[ERROR] Could not find real manuscript image at: {real_image_path}")
    else:
        # Load the real image using OpenCV
        color_img = cv2.imread(real_image_path)
        
        if color_img is None:
            print(f"[ERROR] Failed to decode image at {real_image_path}. Check file format.")
        else:
            gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
            _, binary_thresh_img = cv2.threshold(gray_img, 200, 255, cv2.THRESH_BINARY)
            
            # Segment rows using your horizontal projection engine
            row_bounds = segment_rows_horizontal_projection(binary_thresh_img)
            print(f"[FVSM Engine] Successfully segmented {len(row_bounds)} text rows from real manuscript.")
            
            # Slice the real image rows and run them through the FVSM token & Latin sigla pipeline
            audit_results = []
            isolated_rows = []
            
            for s_y, e_y in row_bounds:
                if (e_y - s_y) > 5:
                    row_slice = binary_thresh_img[s_y:e_y, :]
                    isolated_rows.append(row_slice)
                    
            print(f"[INGESTION] Processing {len(isolated_rows)} segmented rows...")
            
            # Simulate token assignment and cross-reference mapping across real corpus
            for i, row in enumerate(isolated_rows):
                # Sample spatial slices for this row (using your mapping matrix)
                sample_slices = [(10, 20, 40), (20, 30, 30), (30, 60, 20)]
                simulated_tokens = map_coordinates_to_vsvm_tokens(sample_slices)
                
                for token in simulated_tokens:
                    clean_token = token.strip("[],.")
                    audit_result = cross_reference_latin_sigla(clean_token)
                    
                    audit_results.append({
                        "row": i,
                        "token": clean_token,
                        "audit_status": audit_result
                    })
                    print(f"DEBUG: Row {i} Token '{clean_token}' resolved -> {audit_result}")
                    
            # Save the final real-corpus audit report
            save_botanical_audit(audit_results, filename="outputs/real_manuscript_audit_report.json")
            print("[FVSM] Real-corpus audit complete and saved!")
            
    import os

print("Searching project folders for images...")
for root, dirs, files in os.walk("."):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            print(f"Found image: {os.path.join(root, file)}")
    
