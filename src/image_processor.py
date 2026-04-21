import numpy as np
from typing import List

class ImageProcessor:
    def image_negative(self, image: np.ndarray) -> np.ndarray:
        """Apply image negative transformation"""
        return 255 - image
    
    def gamma_correction(self, image: np.ndarray, gamma: float) -> np.ndarray:
        """Apply gamma encoding/correction"""
        normalized = image / 255.0
        corrected = np.power(normalized, gamma)
        output = np.uint8(corrected * 255)
        return output
    
    def log_transformation(self, image: np.ndarray, c: float = 1.0) -> np.ndarray:
        """Apply logarithmic transformation"""
        normalized = image / 255.0
        transformed = c * np.log1p(normalized)
        output = np.uint8(255 * transformed / np.max(transformed))
        return output
    
    def contrast_stretching(self, image: np.ndarray, r1: int, s1: int, 
                           r2: int, s2: int) -> np.ndarray:
        """Apply contrast stretching"""
        output = np.zeros_like(image, dtype=np.float32)
        
        mask1 = image < r1
        if r1 > 0:
            output[mask1] = (s1 / r1) * image[mask1]
        
        mask2 = (image >= r1) & (image <= r2)
        if r2 > r1:
            output[mask2] = ((s2 - s1) / (r2 - r1)) * (image[mask2] - r1) + s1
        
        mask3 = image > r2
        if r2 < 255:
            output[mask3] = ((255 - s2) / (255 - r2)) * (image[mask3] - r2) + s2
        
        return np.uint8(np.clip(output, 0, 255))
    
    def histogram_equalization(self, image: np.ndarray) -> np.ndarray:
        """Apply histogram equalization"""
        hist, bins = np.histogram(image.flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_min = cdf[cdf > 0].min()
        cdf_normalized = ((cdf - cdf_min) * 255) / (cdf[-1] - cdf_min)
        output = np.uint8(cdf_normalized[image])
        return output
    
    def intensity_level_slicing(self, image: np.ndarray, lower: int, 
                                upper: int, preserve: bool = True) -> np.ndarray:
        """Apply intensity level slicing"""
        output = np.zeros_like(image)
        
        if preserve:
            output = image.copy()
            mask = (image >= lower) & (image <= upper)
            output[mask] = 255
        else:
            mask = (image >= lower) & (image <= upper)
            output[mask] = 255
        
        return output
    
    def bit_plane_slicing(self, image: np.ndarray, plane: int) -> np.ndarray:
        """Extract specific bit plane"""
        mask = 1 << plane
        bit_plane = (image & mask) >> plane
        output = bit_plane * 255
        return np.uint8(output)
    
    def extract_all_bit_planes(self, image: np.ndarray) -> List[np.ndarray]:
        """Extract all 8 bit planes"""
        planes = []
        for i in range(8):
            plane = self.bit_plane_slicing(image, i)
            planes.append(plane)
        return planes
