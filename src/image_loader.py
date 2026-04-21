import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple

class ImageLoader:
    def load_image(self, filepath: str, mode: str = 'color') -> np.ndarray:
        """Load image from file"""
        if mode == 'color':
            image = cv2.imread(filepath, cv2.IMREAD_COLOR)
        else:
            image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        
        if image is None:
            raise FileNotFoundError(f"Image not found: {filepath}")
        
        return image
    
    def validate_image(self, image: np.ndarray) -> bool:
        """Validate image array"""
        if image is None or not isinstance(image, np.ndarray):
            return False
        if len(image.shape) not in [2, 3]:
            return False
        return True
    
    def convert_to_grayscale(self, image: np.ndarray) -> np.ndarray:
        """Convert RGB to grayscale"""
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image
    
    def load_batch(self, folder: str) -> List[Tuple[str, np.ndarray]]:
        """Load multiple images from folder"""
        images = []
        folder_path = Path(folder)
        
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
            for filepath in folder_path.glob(ext):
                try:
                    image = self.load_image(str(filepath))
                    images.append((filepath.name, image))
                except Exception as e:
                    print(f"Error loading {filepath}: {e}")
        
        return images
