# Image Processing Assignment - Frequency Domain Filtering and Aliasing

This repository contains solutions to the image processing assignment, which covers tasks such as Gaussian bandpass filtering in the frequency domain, performing DFT/IDFT from scratch, and analyzing aliasing effects in both the frequency and spatial domains. The tasks involve hands-on implementation of Fourier transforms, frequency filtering, and visualizing aliasing effects.

## Tasks

### Task 1: Gaussian Bandpass Filtering in the Frequency Domain
- **Objective**: Perform Gaussian bandpass filtering by cascading Gaussian high and low pass filters in the frequency domain. 
- **Approach**:
  - A Gaussian high pass filter with a cutoff frequency of 100.0.
  - A Gaussian low pass filter with a cutoff frequency of 120.0.
  - Perform DFT and IDFT from scratch and compare the results with OpenCV’s implementation of DFT/IDFT.
- **Input**: `a_3_task_1_input.png`
- **Verification**: The results are verified by comparing them with OpenCV’s implementation of DFT/IDFT.

### Task 2: DFT and IDFT on Two Images
- **Objective**: Perform the DFT on two images, then reconstruct one image using different strategies:
  - Replace the DFT magnitude of Im1 with the DFT magnitude of Im2 to create `Im1_ver1`.
  - Replace the DFT phase of Im1 with the DFT phase of Im2 to create `Im1_ver2`.
- **Objective Question**: Which version of the reconstructed image is closer to the original image, and why?
- **Input**: `a_3_task_2_im1.png` and `a_3_task_2_im2.png`
  
### Task 3: Aliasing in the Frequency and Spatial Domains
- **Objective**: Analyze aliasing effects in both the frequency and spatial domains.
  - **Frequency Domain (Subsampling)**: Perform DFT on an image and show its magnitude spectrum. Then, subsample the image by setting every alternate pixel to 0 and show the magnitude spectrum of the resulting subsampled image.
  - **Spatial Domain (Subsampling in DFT)**: Perform DFT on an image, then subsample the DFT along the horizontal axis by setting every 3rd DFT coefficient to 0. Perform IDFT and observe the effect in the spatial domain.
- **Input**: 
  - For Frequency Domain: `a_3_task_3_input_a.png`
  - For Spatial Domain: `a_3_task_3_input_b.png`
  
## Requirements
- Python 3.x
- NumPy
- OpenCV
- Matplotlib

## Installation

Clone the repository:

```bash
git clone https://github.com/Krishna737Sharma/image-processing-assignment.git
cd image-processing-assignment
