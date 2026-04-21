import matplotlib.pyplot as plt
import numpy as np
import cv2
from typing import List

class Visualizer:
    def plot_comparison(self, original: np.ndarray, processed: np.ndarray,
                       title: str, method_name: str, save_path: str = None) -> None:
        """Create side-by-side comparison plot"""
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        if len(original.shape) == 2:
            axes[0].imshow(original, cmap='gray')
            axes[1].imshow(processed, cmap='gray')
        else:
            axes[0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
            axes[1].imshow(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))
        
        axes[0].set_title('Original Image')
        axes[1].set_title(title)
        axes[0].axis('off')
        axes[1].axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        
        plt.close()
    
    def plot_histogram(self, image: np.ndarray, title: str, save_path: str = None) -> None:
        """Plot image histogram"""
        plt.figure(figsize=(10, 4))
        
        if len(image.shape) == 2:
            hist = cv2.calcHist([image], [0], None, [256], [0, 256])
            plt.plot(hist, color='black')
        else:
            colors = ('b', 'g', 'r')
            for i, color in enumerate(colors):
                hist = cv2.calcHist([image], [i], None, [256], [0, 256])
                plt.plot(hist, color=color)
        
        plt.title(title)
        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        
        plt.close()
    
    def plot_bit_planes(self, image: np.ndarray, planes: List[np.ndarray], save_path: str = None) -> None:
        """Plot all 8 bit planes"""
        fig, axes = plt.subplots(2, 4, figsize=(16, 8))
        
        for i, (ax, plane) in enumerate(zip(axes.flat, planes)):
            ax.imshow(plane, cmap='gray')
            ax.set_title(f'Bit Plane {i}')
            ax.axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        
        plt.close()
