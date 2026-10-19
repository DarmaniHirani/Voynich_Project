"""
Voynich_Project: Folio Matrix Image Preprocessor
Applies adaptive thresholding, bilateral noise reduction, morphological
closings, and reading-order spatial sorting for historical manuscripts.
"""

import cv2
import numpy as np

class FolioMatrixProcessor:
    def __init__(self, target_dpi: int = 300):
        self.target_dpi = target_dpi

    def clean_parchment_texture(self, raw_image_path: str) -> np.ndarray:
        """
        Removes centuries-old parchment noise and fiber artifacts.
        Maintains crisp text edges to protect fine tittle and macron stroke vectors. 
        """
        img = cv2.imread(raw_image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise FileNotFoundError(f"Source scan asset not found at {raw_image_path}")

        # 1. Bilateral Filter: Blurs background texture while keeping text edges sharp
        denoised = cv2.bilateralFilter(img, 9, 75, 75)

        # 2. Adaptive Gaussian Thresholding: Handles uneven aging, stains, and illumination gradients
        binary_matrix = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )

        # 3. Morphological Rectangular Closing: Connects slight breaks in faded ink lines
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        optimized_script_matrix = cv2.morphologyEx(binary_matrix, cv2.MORPH_CLOSE, kernel)

        return optimized_script_matrix

    def extract_bounding_boxes(self, matrix: np.ndarray) -> list:
        """Isolates individual character coordinates to pass straight to FVSM mapping."""
        contours, _ = cv2.findContours(matrix, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        token_coordinates = []
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # Filter out ultra-small noise blobs
            if w > 4 and h > 4:
                token_coordinates.append((x, y, w, h))
                
        return token_coordinates

    def sort_bounding_boxes_by_reading_order(self, coordinates: list, y_tolerance_px: int = 15) -> list:
        """
        Sorts raw bounding box coordinates into chronological Western reading order.
        Groups characters into distinct text rows before sorting from left to right.
        """
        if not coordinates:
            return []

        # 1. Sort all bounding boxes primarily by their top-left Y coordinate
        sorted_by_y = sorted(coordinates, key=lambda box: box[1])
        
        rows = []
        current_row = [sorted_by_y[0]]
        
        # 2. Cluster boxes into rows based on a vertical proximity threshold
        for box in sorted_by_y[1:]:
            x, y, w, h = box
            if y - current_row[-1][1] <= y_tolerance_px:
                current_row.append(box)
            else:
                rows.append(current_row)
                current_row = [box]
        rows.append(current_row)
        
        # 3. Sort each individual row matrix cleanly from left to right (X coordinate)
        final_reading_order = []
        for row in rows:
            sorted_row = sorted(row, key=lambda box: box[0])
            final_reading_order.extend(sorted_row)
            
        return final_reading_order

if __name__ == "__main__":
    print("🤖 Folio image matrix processor engine initialized with spatial reading-order sorting.")
