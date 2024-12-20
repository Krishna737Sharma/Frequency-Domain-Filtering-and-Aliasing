import cv2
import numpy as np
import matplotlib.pyplot as plt

"""###Task 1 Solution"""

def normalized(data):
  data_normalized = (data - np.min(data)) / (np.max(data) - np.min(data))
  return data_normalized * 255.0

def dft_1d(input):
  length = len(input)
  x = []

  for n in range(length):
    x_n = 0

    for k in range(length):
      e = np.exp(-2j * np.pi * k * n / length)
      x_n += input[k] * e

    x.append(x_n)
  return np.array(x)

def dft_2d(input):
  image = np.zeros(input.shape, dtype=np.complex128)
  for col in range(image.shape[1]):
    image[:, col] = dft_1d(input[:, col])

  for row in range(image.shape[0]):
    image[row, :] = dft_1d(image[row,:])

  return image

def idft_1d(input):
  length = len(input)
  x = []

  for n in range(length):
    x_n = 0

    for k in range(length):
      e = np.exp(2j * np.pi * k * n / length)
      x_n += input[k] * e

    x.append(x_n)
  return (np.array(x) / float(length))

def idft_2d(input):
  image = np.zeros(input.shape, dtype=np.complex128)
  for col in range(image.shape[1]):
    image[:, col] = idft_1d(input[:, col])

  for row in range(image.shape[0]):
    image[row, :] = idft_1d(image[row,:])

  return image

def create_gaussian_filter(shape, cutoff, filter_type='low'):
    rows, cols = shape
    crow, ccol = rows // 2, cols // 2
    u = np.arange(0, rows, 1)
    v = np.arange(0, cols, 1)
    u, v = np.meshgrid(u - crow, v - ccol)
    d = np.sqrt(u ** 2 + v ** 2)

    if filter_type == 'low':
        H = np.exp(-d ** 2 / (2 * (cutoff / 3.0) ** 2))
    elif filter_type == 'high':
        H = 1 - np.exp(-d ** 2 / (2 * (cutoff / 3.0) ** 2))
    else:
        raise ValueError("Unknown filter type")

    return H

def shift_2d(input):
  output = np.zeros_like(input)

  output[:(output.shape[0] // 2), :(output.shape[1] // 2)] = input[(input.shape[0] // 2):, (input.shape[1] // 2):]
  output[:(output.shape[0] // 2), (output.shape[1] // 2):] = input[(input.shape[0] // 2):, :(input.shape[1] // 2)]
  output[(output.shape[0] // 2):, :(output.shape[1] // 2)] = input[:(input.shape[0] // 2), (input.shape[1] // 2):]
  output[(output.shape[0] // 2):, (output.shape[1] // 2):] = input[:(input.shape[0] // 2), :(input.shape[1] // 2)]

  return output

image_task_1 = cv2.imread('a_3_task_1_input.png', cv2.IMREAD_GRAYSCALE)
plt.imshow(image_task_1, cmap='gray')
plt.title("Original Image")
plt.show()

freq_from_scratch = dft_2d(image_task_1.astype(np.float32))
freq_shifted_from_scratch = shift_2d(freq_from_scratch)
recon_from_scratch = idft_2d(freq_from_scratch)

freq_cv2 = cv2.dft(image_task_1.astype(np.float32), flags=cv2.DFT_COMPLEX_OUTPUT)
freq_cv2_complex = freq_cv2[:, :, 0] + 1j * freq_cv2[:, :, 1]
freq_shifted_cv2 = np.fft.fftshift(freq_cv2_complex)
recon_image_cv2 = cv2.idft(freq_cv2, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)

plt.figure(figsize=(12.0, 18.0))
plt.subplot(3, 2, 1).imshow(np.log(np.abs(freq_shifted_from_scratch)), cmap='gray')
plt.title("From Scratch: Log-Compressed Magnitude Spectrum")
plt.subplot(3, 2, 2).imshow(np.log(np.abs(freq_shifted_cv2)), cmap='gray')
plt.title("OpenCV: Log-Compressed Magnitude Spectrum")
plt.subplot(3, 2, 3).imshow(np.angle(freq_shifted_from_scratch), cmap='gray')
plt.title("From Scratch: Phase Spectrum")
plt.subplot(3, 2, 4).imshow(np.angle(freq_shifted_cv2), cmap='gray')
plt.title("OpenCV: Phase Spectrum")
plt.subplot(3, 2, 5).imshow(np.real(recon_from_scratch), cmap='gray')
plt.title("From Scratch: Image Reconstruction")
plt.subplot(3, 2, 6).imshow(recon_image_cv2, cmap='gray')
plt.title("OpenCV: Image Reconstruction")
plt.show()

freq = dft_2d(image_task_1.astype(np.float32))
freq_shifted = shift_2d(freq)

freq_magnitude = np.abs(freq_shifted)
freq_phase = np.angle(freq_shifted)

freq_magnitude_bpf = create_gaussian_filter(freq_magnitude.shape, cutoff=100.0, filter_type='high') * create_gaussian_filter(freq_magnitude.shape, cutoff=120.0, filter_type='low') * freq_magnitude
freq_combined = (freq_magnitude_bpf * np.cos(freq_phase)) + 1j * (freq_magnitude_bpf * np.sin(freq_phase))

recon_image = idft_2d(shift_2d(freq_combined))

freq_cv2 = cv2.dft(image_task_1.astype(np.float32), flags=cv2.DFT_COMPLEX_OUTPUT)
freq_cv2_complex = freq_cv2[:, :, 0] + 1j * freq_cv2[:, :, 1]
freq_shifted_cv2 = shift_2d(freq_cv2_complex)

freq_magnitude_cv2 = np.abs(freq_shifted_cv2)
freq_phase_cv2 = np.angle(freq_shifted_cv2)

freq_magnitude_bpf_cv2 = create_gaussian_filter(freq_magnitude.shape, cutoff=100.0, filter_type='high') * create_gaussian_filter(freq_magnitude.shape, cutoff=120.0, filter_type='low') * freq_magnitude_cv2
freq_combined_cv2 = (freq_magnitude_bpf_cv2 * np.cos(freq_phase_cv2)) + 1j * (freq_magnitude_bpf_cv2 * np.sin(freq_phase_cv2))

freq_combined_cv2_shifted = shift_2d(freq_combined_cv2)

cv2_channels = np.array([np.real(freq_combined_cv2_shifted), np.imag(freq_combined_cv2_shifted)]).transpose(1, 2, 0)

recon_image_cv2 = cv2.idft(cv2_channels, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)

plt.figure(figsize=(12.0, 18.0))
plt.subplot(3, 2, 1).imshow(np.log(freq_magnitude), cmap='gray')
plt.title("Magnitude Spectrum: Without Filtering (From Scratch)")
plt.subplot(3, 2, 2).imshow(np.log(freq_magnitude_cv2), cmap='gray')
plt.title("Magnitude Spectrum: Without Filtering (OpenCV)")
plt.subplot(3, 2, 3).imshow(np.log(freq_magnitude_bpf + 1.0), cmap='gray')
plt.title("Magnitude Spectrum: With Gaussian BPF (From Scratch)")
plt.subplot(3, 2, 4).imshow(np.log(freq_magnitude_bpf_cv2 + 1.0), cmap='gray')
plt.title("Magnitude Spectrum: With Gaussian BPF (OpenCV)")
plt.subplot(3, 2, 5).imshow(np.real(recon_image), cmap='gray')
plt.title("Reconstruction: With Gaussian BPF (From Scratch)")
plt.subplot(3, 2, 6).imshow(np.real(recon_image_cv2), cmap='gray')
plt.title("Reconstruction: With Gaussian BPF (OpenCV)")
plt.show()

"""###Task 2 Solution"""

image_task_2_im1 = cv2.imread('a_3_task_2_im1.png', cv2.IMREAD_GRAYSCALE)
image_task_2_im2 = cv2.imread('a_3_task_2_im2.png', cv2.IMREAD_GRAYSCALE)

plt.figure(figsize=(12.0, 6.0))
plt.subplot(1, 2, 1).imshow(image_task_2_im1, cmap='gray')
plt.title("Image Im1")
plt.subplot(1, 2, 2).imshow(image_task_2_im2, cmap='gray')
plt.title("Image Im2")
plt.show()

freq_im1 = dft_2d(image_task_2_im1.astype(np.float32))
freq_shifted_im1 = shift_2d(freq_im1)

freq_magnitude_im1 = np.abs(freq_shifted_im1)
freq_phase_im1 = np.angle(freq_shifted_im1)

freq_im2 = dft_2d(image_task_2_im2.astype(np.float32))
freq_shifted_im2 = shift_2d(freq_im2)

freq_magnitude_im2 = np.abs(freq_shifted_im2)
freq_phase_im2 = np.angle(freq_shifted_im2)

freq_combined_ver1 = (freq_magnitude_im2 * np.cos(freq_phase_im1)) + 1j * (freq_magnitude_im2 * np.sin(freq_phase_im1))
freq_combined_ver2 = (freq_magnitude_im1 * np.cos(freq_phase_im2)) + 1j * (freq_magnitude_im1 * np.sin(freq_phase_im2))

output_ver1 = idft_2d(shift_2d(freq_combined_ver1))
output_ver2 = idft_2d(shift_2d(freq_combined_ver2))

plt.figure(figsize=(12.0, 6.0))
plt.subplot(1, 2, 1).imshow(np.real(output_ver1), cmap='gray')
plt.title("Output Image Im1_ver1")
plt.subplot(1, 2, 2).imshow(np.real(output_ver2), cmap='gray')
plt.title("Output Image Im1_ver2")
plt.show()

"""Out of the two outputs, Im1_ver1 is closer to Im1 because the phase information is still intact. While the brightness levels are wrong due to change in magnitude spectrum, the overall structure is still maintained due to unchanged phase spectrum.

### Task 3 Solution

Aliasing in frequency domain
"""

image_task_3_im1 = cv2.imread('a_3_task_3_input_a.png', cv2.IMREAD_GRAYSCALE)
image_subsampled = image_task_3_im1.copy()
image_subsampled[::2, :] = 0.0
image_subsampled[:, ::2] = 0.0

freq_im1 = dft_2d(image_task_3_im1.astype(np.float32))
freq_shifted_im1 = shift_2d(freq_im1)
freq_magnitude_im1 = np.abs(freq_shifted_im1)

freq_im1_sub = dft_2d(image_subsampled.astype(np.float32))
freq_shifted_im1_sub = shift_2d(freq_im1_sub)
freq_magnitude_im1_sub = np.abs(freq_shifted_im1_sub)

plt.figure(figsize=(12.0, 12.0))
plt.subplot(2, 2, 1).imshow(image_task_3_im1, cmap='gray')
plt.title("Original Task 3 Image 1")
plt.subplot(2, 2, 2).imshow(image_subsampled, cmap='gray')
plt.title("Subsampled Task 3 Image 1")
plt.subplot(2, 2, 3).imshow(np.log(freq_magnitude_im1), cmap='gray')
plt.title("Original Magnitude Spectrum")
plt.subplot(2, 2, 4).imshow(np.log(freq_magnitude_im1_sub), cmap='gray')
plt.title("Magnitude Spectrum of Subsampled Image")
plt.show()

"""Aliasing in spatial domain"""

image_task_3_im2 = cv2.imread('a_3_task_3_input_b.png', cv2.IMREAD_GRAYSCALE)

freq_im1 = dft_2d(image_task_3_im2.astype(np.float32))
freq_im1 = shift_2d(freq_im1)
freq_im_1_subsampled = freq_im1.copy()
freq_im_1_subsampled[:, ::3] = 0.0 + 0.0j

freq_im1_shifted = shift_2d(freq_im1)
freq_im1_subsampled_shifted = shift_2d(freq_im_1_subsampled)

image_recon_im1 = idft_2d(freq_im1_shifted)
image_recon_im1_sub = idft_2d(freq_im1_subsampled_shifted)



plt.figure(figsize=(12.0, 18.0))
plt.subplot(3, 2, 1).imshow(np.log(np.abs(freq_im1)), cmap='gray')
plt.title("Original Magnitude Spectrum (Task 3 Image 2)")
plt.subplot(3, 2, 2).imshow(np.log(np.abs(freq_im_1_subsampled) + 1.0), cmap='gray')
plt.title("Subsampled Magnitude Spectrum (Task 3 Image 2)")
plt.subplot(3, 2, 3).imshow(np.angle(freq_im1), cmap='gray')
plt.title("Original Phase Spectrum (Task 3 Image 2)")
plt.subplot(3, 2, 4).imshow(np.angle(freq_im_1_subsampled), cmap='gray')
plt.title("Subsampled Phase Spectrum of (Task 3 Image 2)")
plt.subplot(3, 2, 5).imshow(np.real(image_recon_im1), cmap='gray')
plt.title("Original Image Reconstruction (Task 3 Image 2)")
plt.subplot(3, 2, 6).imshow(np.real(image_recon_im1_sub), cmap='gray')
plt.title("Original Image Reconstruction from Subsampled DFT")
plt.show()

"""In the reconstructed image corresponding to the subsampled DFT, image seems to replicate three times in the horizontal direction. This is because subsampling the DFT results in aliasing in spatial domain."""

