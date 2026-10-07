import os
import cv2
import numpy as np

class FolioMatrixProcessor:
    def __init__(self, input_dir="raw_folios", output_dir="normalized_matrices"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.target_vectors = ['T', 'I', 'R', 'D', 'A', 'O', 'S', 'C', 'F', 'P']
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"[INITIALIZED] Phase 2 Workspace Matrix Created.")
        
    def execute_topological_grayscale_filter(self, image_path):
        if not os.path.exists(image_path):
            return None
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 8)

    def extract_glyph_coordinate_slices(self, processed_matrix, min_glyph_area=12):
        if processed_matrix is None:
            return []
        contours, _ = cv2.findContours(processed_matrix, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        coordinate_slices = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > min_glyph_area:
                x, y, w, h = cv2.boundingRect(cnt)
                coordinate_slices.append({"box": (int(x), int(y), int(w), int(h)), "area": int(area)})
        return sorted(coordinate_slices, key=lambda b: ((b['box'][1] // 25) * 1000 + b['box'][0]))

    def export_normalized_matrix_grid(self, coordinate_slices, source_filename):
        if not coordinate_slices:
            return None
        matrix_array = np.array([b['box'] for b in coordinate_slices], dtype=np.float32)
        x_min, y_min = np.min(matrix_array[:, 0]), np.min(matrix_array[:, 1])
        x_max, y_max = np.max(matrix_array[:, 0] + matrix_array[:, 2]), np.max(matrix_array[:, 1] + matrix_array[:, 3])
        
        range_x = max(x_max - x_min, 1.0)
        range_y = max(y_max - y_min, 1.0)
        
        normalized_array = np.copy(matrix_array)
        normalized_array[:, 0] = (matrix_array[:, 0] - x_min) / range_x
        normalized_array[:, 1] = (matrix_array[:, 1] - y_min) / range_y
        normalized_array[:, 2] = matrix_array[:, 2] / range_x
        normalized_array[:, 3] = matrix_array[:, 3] / range_y

        base_name = os.path.splitext(source_filename)[0]
        output_filepath = os.path.join(self.output_dir, f"{base_name}_matrix.npy")
        np.save(output_filepath, normalized_array)
        print(f"[EXPORT SUCCESS] Normalized matrix saved to: {output_filepath}")
        return output_filepath

if __name__ == "__main__":
    processor = FolioMatrixProcessor()
    sample_path = os.path.join(processor.input_dir, "sample_folio.jpg")
    if not os.path.exists(sample_path):
        synthetic_folio = np.ones((400, 600, 3), dtype=np.uint8) * 235
        for row in range(5):
            y_pos = 70 + (row * 60)
            for col in range(12):
                x_pos = 50 + (col * 40)
                cv2.rectangle(synthetic_folio, (x_pos, y_pos), (x_pos + 18, y_pos + 28), (40, 30, 20), -1)
        cv2.imwrite(sample_path, synthetic_folio)
    matrix = processor.execute_topological_grayscale_filter(sample_path)
    slices = processor.extract_glyph_coordinate_slices(matrix)
    processor.export_normalized_matrix_grid(slices, "sample_folio.jpg")
