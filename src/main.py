import cv2
import numpy as np
from pathlib import Path
from image_loader import ImageLoader
from image_processor import ImageProcessor
from visualizer import Visualizer
from output_manager import OutputManager

def process_rgb_image(processor: ImageProcessor, image_rgb: np.ndarray, method: str, **params) -> np.ndarray:
    """Process RGB image by applying method to each channel"""
    b, g, r = cv2.split(image_rgb)
    
    if method == 'negative':
        b_proc = processor.image_negative(b)
        g_proc = processor.image_negative(g)
        r_proc = processor.image_negative(r)
    elif method == 'gamma':
        gamma = params.get('gamma', 0.5)
        b_proc = processor.gamma_correction(b, gamma)
        g_proc = processor.gamma_correction(g, gamma)
        r_proc = processor.gamma_correction(r, gamma)
    elif method == 'log':
        c = params.get('c', 1.0)
        b_proc = processor.log_transformation(b, c)
        g_proc = processor.log_transformation(g, c)
        r_proc = processor.log_transformation(r, c)
    elif method == 'contrast':
        r1, s1, r2, s2 = params.get('r1', 50), params.get('s1', 0), params.get('r2', 200), params.get('s2', 255)
        b_proc = processor.contrast_stretching(b, r1, s1, r2, s2)
        g_proc = processor.contrast_stretching(g, r1, s1, r2, s2)
        r_proc = processor.contrast_stretching(r, r1, s1, r2, s2)
    elif method == 'histogram':
        b_proc = processor.histogram_equalization(b)
        g_proc = processor.histogram_equalization(g)
        r_proc = processor.histogram_equalization(r)
    elif method == 'intensity':
        lower, upper = params.get('lower', 100), params.get('upper', 200)
        b_proc = processor.intensity_level_slicing(b, lower, upper)
        g_proc = processor.intensity_level_slicing(g, lower, upper)
        r_proc = processor.intensity_level_slicing(r, lower, upper)
    elif method == 'bitplane':
        plane = params.get('plane', 7)
        b_proc = processor.bit_plane_slicing(b, plane)
        g_proc = processor.bit_plane_slicing(g, plane)
        r_proc = processor.bit_plane_slicing(r, plane)
    else:
        return image_rgb
    
    result = cv2.merge([b_proc, g_proc, r_proc])
    return result

def main():
    # Initialize components
    loader = ImageLoader()
    processor = ImageProcessor()
    visualizer = Visualizer()
    output_mgr = OutputManager()
    
    # Setup folders
    output_mgr.setup_folders()
    print("Folder structure created successfully!")
    
    # Load images (adjust path based on where script is run from)
    input_folder = Path('../images/input')
    if not input_folder.exists():
        input_folder = Path('images/input')
    
    images = loader.load_batch(str(input_folder))
    
    if not images:
        print(f"No images found in {input_folder}")
        print("Please add images to the 'images/input' folder and run again.")
        return
    
    print(f"Found {len(images)} images to process")
    
    results = {}
    
    # Process each image
    for filename, image in images:
        print(f"\nProcessing {filename}...")
        
        # Convert to grayscale
        gray = loader.convert_to_grayscale(image)
        
        # 1. Image Negative
        negative = processor.image_negative(gray)
        output_mgr.save_processed_image(negative, 'negative', filename)
        results_path = output_mgr.results_path / f'{Path(filename).stem}_negative.png'
        visualizer.plot_comparison(gray, negative, 'Image Negative', 'negative', str(results_path))
        
        # 2. Gamma Correction
        gamma = processor.gamma_correction(gray, gamma=0.5)
        output_mgr.save_processed_image(gamma, 'gamma', filename)
        results_path = output_mgr.results_path / f'{Path(filename).stem}_gamma.png'
        visualizer.plot_comparison(gray, gamma, 'Gamma Correction (γ=0.5)', 'gamma', str(results_path))
        
        # 3. Log Transformation
        log_trans = processor.log_transformation(gray)
        output_mgr.save_processed_image(log_trans, 'log', filename)
        results_path = output_mgr.results_path / f'{Path(filename).stem}_log.png'
        visualizer.plot_comparison(gray, log_trans, 'Log Transformation', 'log', str(results_path))
        
        # 4. Contrast Stretching
        contrast = processor.contrast_stretching(gray, 50, 0, 200, 255)
        output_mgr.save_processed_image(contrast, 'contrast', filename)
        results_path = output_mgr.results_path / f'{Path(filename).stem}_contrast.png'
        visualizer.plot_comparison(gray, contrast, 'Contrast Stretching', 'contrast', str(results_path))
        
        # 5. Histogram Equalization
        hist_eq = processor.histogram_equalization(gray)
        output_mgr.save_processed_image(hist_eq, 'histogram', filename)
        results_path = output_mgr.results_path / f'{Path(filename).stem}_histogram.png'
        visualizer.plot_comparison(gray, hist_eq, 'Histogram Equalization', 'histogram', str(results_path))
        
        # 6. Intensity Level Slicing
        intensity_slice = processor.intensity_level_slicing(gray, 100, 200)
        output_mgr.save_processed_image(intensity_slice, 'intensity', filename)
        results_path = output_mgr.results_path / f'{Path(filename).stem}_intensity.png'
        visualizer.plot_comparison(gray, intensity_slice, 'Intensity Level Slicing', 'intensity', str(results_path))
        
        # 7. Bit Plane Slicing
        bit_plane = processor.bit_plane_slicing(gray, 7)
        output_mgr.save_processed_image(bit_plane, 'bitplane', filename)
        all_planes = processor.extract_all_bit_planes(gray)
        results_path = output_mgr.results_path / f'{Path(filename).stem}_bitplanes.png'
        visualizer.plot_bit_planes(gray, all_planes, str(results_path))
        
        print(f"✓ Completed processing {filename}")
    
    print("\n" + "="*50)
    print("Processing complete!")
    print(f"Processed images saved to: {output_mgr.output_path}")
    print(f"Visualizations saved to: {output_mgr.results_path}")
    print("="*50)

if __name__ == '__main__':
    main()
