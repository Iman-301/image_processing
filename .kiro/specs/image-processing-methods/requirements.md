# Requirements Document: Image Processing Methods

## Introduction

This document specifies the functional and business requirements for a Digital Image Processing system that implements 7 fundamental image transformation methods. The system processes both RGB and grayscale images, applies various transformations, and generates visualizations for academic demonstration and reporting purposes. The implementation targets educational use in a Digital Image Processing course assignment.

## Glossary

- **System**: The complete image processing application including all components
- **ImageLoader**: Component responsible for loading and validating images from disk
- **ImageProcessor**: Component that applies transformation algorithms to images
- **Visualizer**: Component that creates comparison plots and visualizations
- **OutputManager**: Component that manages folder structure and file organization
- **Transformation**: An image processing method that converts input pixels to output pixels
- **Bit_Plane**: A binary image representing a single bit position across all pixels
- **Histogram**: Statistical distribution of pixel intensity values
- **CDF**: Cumulative Distribution Function of pixel intensities
- **Grayscale_Image**: Single-channel image with intensity values [0, 255]
- **RGB_Image**: Three-channel color image with separate red, green, and blue channels

## Requirements

### Requirement 1: Image Loading and Validation

**User Story:** As a user, I want to load images from disk, so that I can process them with various transformation methods.

#### Acceptance Criteria

1. WHEN a valid image file path is provided, THE ImageLoader SHALL load the image into a numpy array
2. WHEN an image file is not found, THE ImageLoader SHALL raise a FileNotFoundError with a descriptive message
3. WHEN a corrupted image file is provided, THE ImageLoader SHALL handle the error gracefully and skip to the next image
4. THE ImageLoader SHALL support JPEG, PNG, and BMP file formats
5. WHEN loading multiple images from a folder, THE ImageLoader SHALL return a list of tuples containing filename and image array pairs
6. WHEN an RGB image is loaded, THE ImageLoader SHALL provide conversion to grayscale format
7. THE ImageLoader SHALL validate that loaded images have valid dimensions and data types

### Requirement 2: Image Negative Transformation

**User Story:** As a user, I want to apply image negative transformation, so that I can invert the intensity values of an image.

#### Acceptance Criteria

1. WHEN an image is provided, THE ImageProcessor SHALL compute the negative using the formula: output = 255 - input
2. THE ImageProcessor SHALL preserve the shape and dimensions of the input image
3. THE ImageProcessor SHALL ensure output values remain in the range [0, 255]
4. THE ImageProcessor SHALL support both grayscale and RGB images for negative transformation
5. WHEN processing RGB images, THE ImageProcessor SHALL apply the transformation to each channel independently

### Requirement 3: Gamma Correction

**User Story:** As a user, I want to apply gamma correction, so that I can adjust image brightness using power-law transformation.

#### Acceptance Criteria

1. WHEN a gamma value is provided, THE ImageProcessor SHALL apply the power-law transformation: output = input^gamma
2. WHEN gamma is less than 1, THE ImageProcessor SHALL brighten the image
3. WHEN gamma is greater than 1, THE ImageProcessor SHALL darken the image
4. WHEN gamma equals 1, THE ImageProcessor SHALL return an image equivalent to the input
5. IF gamma is less than or equal to 0, THEN THE ImageProcessor SHALL raise a ValueError
6. THE ImageProcessor SHALL normalize pixel values to [0, 1] before applying gamma, then scale back to [0, 255]
7. THE ImageProcessor SHALL support gamma values in the typical range of 0.1 to 5.0

### Requirement 4: Logarithmic Transformation

**User Story:** As a user, I want to apply logarithmic transformation, so that I can expand dark pixel values and compress bright values.

#### Acceptance Criteria

1. WHEN an image is provided, THE ImageProcessor SHALL apply the formula: output = c * log(1 + input)
2. THE ImageProcessor SHALL use a default scaling constant c = 1.0 unless specified otherwise
3. THE ImageProcessor SHALL add 1 to pixel values before applying logarithm to prevent log(0)
4. THE ImageProcessor SHALL normalize the output to the range [0, 255]
5. WHEN the scaling constant c is provided, THE ImageProcessor SHALL validate that c is greater than 0

### Requirement 5: Contrast Stretching

**User Story:** As a user, I want to apply contrast stretching, so that I can enhance image contrast using piecewise linear transformation.

#### Acceptance Criteria

1. WHEN control points (r1, s1, r2, s2) are provided, THE ImageProcessor SHALL apply piecewise linear transformation
2. THE ImageProcessor SHALL validate that 0 ≤ r1 < r2 ≤ 255
3. THE ImageProcessor SHALL validate that 0 ≤ s1 < s2 ≤ 255
4. THE ImageProcessor SHALL map the range [0, r1] to [0, s1] using linear interpolation
5. THE ImageProcessor SHALL map the range [r1, r2] to [s1, s2] using linear interpolation
6. THE ImageProcessor SHALL map the range [r2, 255] to [s2, 255] using linear interpolation
7. THE ImageProcessor SHALL ensure output values are clipped to [0, 255]

### Requirement 6: Histogram Equalization

**User Story:** As a user, I want to apply histogram equalization, so that I can enhance image contrast by redistributing intensity values.

#### Acceptance Criteria

1. WHEN a grayscale image is provided, THE ImageProcessor SHALL compute the histogram of pixel intensities
2. THE ImageProcessor SHALL compute the cumulative distribution function (CDF) from the histogram
3. THE ImageProcessor SHALL normalize the CDF to the range [0, 255]
4. THE ImageProcessor SHALL map each input pixel to its equalized value using the normalized CDF
5. THE ImageProcessor SHALL ensure the output histogram is approximately uniform
6. WHEN an RGB image is provided, THE ImageProcessor SHALL convert it to grayscale before equalization
7. THE ImageProcessor SHALL ensure the CDF is monotonically increasing

### Requirement 7: Intensity Level Slicing

**User Story:** As a user, I want to apply intensity level slicing, so that I can highlight specific intensity ranges in an image.

#### Acceptance Criteria

1. WHEN intensity bounds (lower, upper) are provided, THE ImageProcessor SHALL validate that 0 ≤ lower < upper ≤ 255
2. WHEN preserve mode is True, THE ImageProcessor SHALL set pixels in range [lower, upper] to 255 and preserve other pixels
3. WHEN preserve mode is False, THE ImageProcessor SHALL set pixels in range [lower, upper] to 255 and other pixels to 0
4. THE ImageProcessor SHALL classify each pixel as either in-range or out-of-range
5. THE ImageProcessor SHALL ensure output values are either 0, 255, or original pixel values depending on mode

### Requirement 8: Bit Plane Slicing

**User Story:** As a user, I want to extract bit planes from an image, so that I can analyze the contribution of each bit position.

#### Acceptance Criteria

1. WHEN a bit plane index (0-7) is provided, THE ImageProcessor SHALL extract that specific bit plane
2. THE ImageProcessor SHALL validate that the plane index is in the range [0, 7]
3. THE ImageProcessor SHALL use bitwise AND operation with mask 2^plane to extract the bit
4. THE ImageProcessor SHALL scale the binary output to [0, 255] for visualization
5. THE ImageProcessor SHALL support extraction of all 8 bit planes from an image
6. WHEN extracting all bit planes, THE ImageProcessor SHALL return them ordered from LSB (plane 0) to MSB (plane 7)
7. THE ImageProcessor SHALL ensure bit plane output contains only values 0 or 255

### Requirement 9: Visualization Generation

**User Story:** As a user, I want to generate side-by-side comparison visualizations, so that I can demonstrate the effects of each transformation method.

#### Acceptance Criteria

1. WHEN original and processed images are provided, THE Visualizer SHALL create a side-by-side comparison plot
2. THE Visualizer SHALL display the original image on the left and processed image on the right
3. THE Visualizer SHALL include a descriptive title indicating the transformation method
4. THE Visualizer SHALL save visualizations in high resolution suitable for presentations
5. WHEN histogram equalization is applied, THE Visualizer SHALL plot histograms of both input and output images
6. WHEN bit plane slicing is applied, THE Visualizer SHALL display all 8 bit planes in a grid layout
7. THE Visualizer SHALL use matplotlib for all visualization generation

### Requirement 10: Output Organization

**User Story:** As a user, I want processed images organized in a structured folder hierarchy, so that I can easily locate and present results.

#### Acceptance Criteria

1. THE OutputManager SHALL create an output directory structure with separate folders for each method
2. THE OutputManager SHALL create folders: negative, gamma, log, contrast, histogram, intensity, and bitplane
3. THE OutputManager SHALL save processed images with descriptive filenames including method name and original filename
4. THE OutputManager SHALL save comparison visualizations in a results folder
5. THE OutputManager SHALL generate a summary report listing all processed images and methods applied
6. WHEN output folders already exist, THE OutputManager SHALL not raise errors
7. IF the output directory is not writable, THEN THE OutputManager SHALL raise a PermissionError

### Requirement 11: Batch Processing

**User Story:** As a user, I want to process multiple images with all methods in a single run, so that I can efficiently generate results for demonstration.

#### Acceptance Criteria

1. WHEN a folder path is provided, THE System SHALL load all supported images from that folder
2. THE System SHALL apply all 7 transformation methods to each loaded image
3. THE System SHALL generate visualizations for each image-method combination
4. THE System SHALL save all processed images to appropriate output folders
5. WHEN an error occurs processing one image, THE System SHALL log the error and continue with remaining images
6. THE System SHALL display completion status after batch processing finishes
7. THE System SHALL process images in a deterministic order (alphabetically by filename)

### Requirement 12: Parameter Validation

**User Story:** As a developer, I want comprehensive parameter validation, so that invalid inputs are caught early with clear error messages.

#### Acceptance Criteria

1. WHEN invalid parameters are provided to any method, THE System SHALL raise a ValueError with parameter constraints
2. THE System SHALL validate that image arrays are not empty
3. THE System SHALL validate that image arrays have valid shapes: (H, W) or (H, W, 3)
4. THE System SHALL validate that image data type is uint8 or convertible to uint8
5. THE System SHALL validate file paths to prevent directory traversal attacks
6. THE System SHALL limit maximum image dimensions to prevent memory exhaustion
7. IF validation fails, THEN THE System SHALL provide a descriptive error message indicating which parameter is invalid

### Requirement 13: RGB Image Support

**User Story:** As a user, I want to process RGB color images, so that I can apply transformations to color photographs.

#### Acceptance Criteria

1. WHEN an RGB image is provided, THE System SHALL detect it has 3 channels
2. THE System SHALL split RGB images into separate color channels
3. THE System SHALL apply transformations to each channel independently
4. THE System SHALL merge processed channels back into an RGB image
5. WHEN histogram equalization is requested for RGB, THE System SHALL convert to grayscale first
6. THE System SHALL preserve color channel order (BGR for OpenCV compatibility)

### Requirement 14: Type and Shape Consistency

**User Story:** As a developer, I want all transformations to maintain consistent data types and shapes, so that outputs can be reliably chained and visualized.

#### Acceptance Criteria

1. THE System SHALL ensure all output images have dtype uint8
2. THE System SHALL ensure output image shape equals input image shape
3. THE System SHALL ensure all output pixel values are in the range [0, 255]
4. THE System SHALL clip any values outside [0, 255] to the valid range
5. WHEN processing operations produce float values, THE System SHALL convert them to uint8 before returning

### Requirement 15: Performance Requirements

**User Story:** As a user, I want fast image processing, so that I can quickly generate results for multiple images.

#### Acceptance Criteria

1. THE System SHALL process a single 1024x768 image in less than 100ms per method
2. THE System SHALL complete batch processing of 10 images in less than 5 seconds total
3. THE System SHALL generate a comparison visualization in less than 500ms
4. THE System SHALL use vectorized NumPy operations instead of pixel-by-pixel loops
5. WHERE parallel processing is available, THE System SHALL process multiple images concurrently

### Requirement 16: Error Recovery

**User Story:** As a user, I want the system to handle errors gracefully, so that one failure doesn't stop the entire batch process.

#### Acceptance Criteria

1. WHEN a file cannot be loaded, THE System SHALL log the error and continue with the next file
2. WHEN processing fails for one method, THE System SHALL continue with remaining methods
3. WHEN memory errors occur, THE System SHALL suggest image resizing and terminate gracefully
4. THE System SHALL maintain a log of all errors encountered during batch processing
5. THE System SHALL display a summary of successful and failed operations at completion

### Requirement 17: Deterministic Behavior

**User Story:** As a developer, I want deterministic processing results, so that the same input always produces the same output.

#### Acceptance Criteria

1. THE System SHALL produce identical output when given identical input and parameters
2. THE System SHALL not use random number generation in any transformation
3. THE System SHALL process images in a consistent order during batch operations
4. THE System SHALL use consistent rounding methods for float-to-int conversions

### Requirement 18: Test Image Recommendations

**User Story:** As a user, I want guidance on selecting test images, so that I can effectively demonstrate each transformation method.

#### Acceptance Criteria

1. THE System documentation SHALL recommend using low-contrast images for contrast stretching
2. THE System documentation SHALL recommend using dark images for gamma correction with γ < 1
3. THE System documentation SHALL recommend using bright images for gamma correction with γ > 1
4. THE System documentation SHALL recommend using medical X-rays for intensity level slicing
5. THE System documentation SHALL recommend using text documents for bit plane slicing
6. THE System documentation SHALL recommend testing each method with at least 2-3 different images
