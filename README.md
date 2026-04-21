# Digital Image Processing - Elementary Methods

Implementation of 7 fundamental image processing methods in Python.

## Methods Implemented

1. Image Negative
2. Gamma Encoding/Correction
3. Logarithmic Transformation
4. Contrast Stretching
5. Histogram Equalization
6. Intensity Level Slicing
7. Bit Plane Slicing

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Place your test images in the `images/input/` folder
2. Run the main script:

```bash
cd src
python main.py
```

3. Results will be saved in:
   - `images/output/` - Processed images organized by method
   - `images/results/` - Comparison visualizations for PPT

## Folder Structure

```
├── images/
│   ├── input/          # Place your test images here
│   ├── output/         # Processed images
│   └── results/        # Visualizations for PPT
├── src/
│   ├── image_loader.py
│   ├── image_processor.py
│   ├── visualizer.py
│   ├── output_manager.py
│   └── main.py
├── requirements.txt
└── README.md
```

## Features

- Handles both RGB and grayscale images
- Automatic folder structure creation
- Side-by-side comparison visualizations
- Batch processing of multiple images
- High-resolution output for presentations
