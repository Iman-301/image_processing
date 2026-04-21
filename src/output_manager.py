import cv2
import numpy as np
from pathlib import Path
from typing import Dict

class OutputManager:
    def __init__(self, base_path: str = 'images'):
        # Adjust path based on where script is run from
        base = Path(base_path)
        if not base.exists():
            base = Path('..') / base
        self.base_path = base
        self.output_path = self.base_path / 'output'
        self.results_path = self.base_path / 'results'
    
    def setup_folders(self) -> None:
        """Create output directory structure"""
        folders = [
            self.base_path / 'input',
            self.output_path / 'negative',
            self.output_path / 'gamma',
            self.output_path / 'log',
            self.output_path / 'contrast',
            self.output_path / 'histogram',
            self.output_path / 'intensity',
            self.output_path / 'bitplane',
            self.results_path
        ]
        
        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)
    
    def save_processed_image(self, image: np.ndarray, method: str, 
                            filename: str) -> str:
        """Save processed image to appropriate folder"""
        output_folder = self.output_path / method
        output_file = output_folder / filename
        cv2.imwrite(str(output_file), image)
        return str(output_file)
    
    def generate_summary_report(self, results: Dict) -> None:
        """Generate summary of all processing results"""
        report_path = self.base_path / 'processing_summary.txt'
        
        with open(report_path, 'w') as f:
            f.write("Image Processing Summary Report\n")
            f.write("=" * 50 + "\n\n")
            
            for method, files in results.items():
                f.write(f"{method.upper()}:\n")
                for file in files:
                    f.write(f"  - {file}\n")
                f.write("\n")
