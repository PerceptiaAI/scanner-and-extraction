# 📄 Document Scanner & OCR Tool

Welcome to the **Document Scanner & OCR Tool**! This Python-based desktop application and command-line script let you easily scan and transform documents by detecting edges and adjusting for perspective, enabling accurate text extraction via OCR (Optical Character Recognition).

## ✨ Features

- **Easy Image Import**: Load images or directories in one step.
- **Document Scanning with Perspective Transformation**: Pre-processes images, detecting and transforming document edges for clear OCR.
- **Interactive Mode**: Adjust document corners manually for precise results.
- **Save & Share Results**: Quickly save processed images and extracted text.

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/PerceptiaAI/scanner-and-extraction.git
   cd scanner-and-extraction
   ```

2. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the GUI Application**:
   ```bash
   python main.py
   ```

4. **Run the Command-Line Script**:
   ```bash
   python scan.py (--images <IMG_DIR> | --image <IMG_PATH>) [-i]
   ```

## 🖼️ GUI Preview

![Document Scanner GUI](https://github.com/PerceptiaAI/scanner-and-extraction/blob/main/docscanner%20screenshot.png)

## 📚 Command-Line Usage

### Usage:
The command-line script supports single-image or batch processing with optional interactive corner adjustment:
- **Single Image**: `python scan.py --image <IMG_PATH> -i`
- **Directory of Images**: `python scan.py --images <IMG_DIR>`

For example:
- To scan a single image with interactive mode:
  ```bash
  python scan.py --image sample_images/desk.JPG -i
  ```
- To scan all images in a directory automatically:
  ```bash
  python scan.py --images sample_images
  ```

### Output:
Processed images will be saved to a directory named `output`.

## 🛠️ Built With

- **Python** 🐍
- **PyQt6**: For the user-friendly and responsive interface.
- **OpenCV**: For image processing, edge detection, and transformations.
- **EasyOCR**: A powerful OCR engine for text extraction.

## 💡 Description of the Core Components

The core of the application is the `DocScanner` class, which scans documents from images by performing the following steps:

1. **Edge Detection**: Detects the edges of the document using the LSD (Line Segment Detector) and Canny edge detection, separating vertical and horizontal lines to form corners.
2. **Perspective Transformation**: Adjusts the document's orientation by transforming the detected corners, aligning it for accurate text recognition.
3. **Interactive Mode**: Allows users to manually adjust corners in a popup window for higher accuracy.
4. **Adaptive Thresholding**: Converts images to a clear black-and-white format for easy readability.
5. **File Output**: Saves the processed, scanned images to an output folder.

## 📥 Installation & Requirements

The application requires Python 3.7+ and the following packages:
- `PyQt6`
- `OpenCV`
- `EasyOCR`
- `Matplotlib`
  
Install all dependencies via:
```bash
pip install -r requirements.txt
```

---

Feel free to contribute or submit any issues you encounter. Happy scanning!
