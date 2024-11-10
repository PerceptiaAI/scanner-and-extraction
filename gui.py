import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                            QVBoxLayout, QPushButton, QLabel, QFileDialog, 
                            QScrollArea, QTextEdit, QMessageBox)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QSize
import cv2
import easyocr
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')  # This is important for matplotlib to work with PyQt

class DocumentScannerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Document Scanner & OCR")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize EasyOCR
        self.reader = easyocr.Reader(['en'], gpu=True)
        
        # Initialize variables
        self.original_image_path = None
        self.scanned_image_path = None
        
        # Ensure output directory exists
        if not os.path.exists('output'):
            os.makedirs('output')
        
        self.init_ui()
        
    def init_ui(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create horizontal layout for image displays
        display_layout = QHBoxLayout()
        
        # Create three display sections
        self.original_display = self.create_display_section("Original Image")
        self.scanned_display = self.create_display_section("Scanned Image")
        self.text_display = self.create_text_section("Extracted Text")
        
        display_layout.addWidget(self.original_display)
        display_layout.addWidget(self.scanned_display)
        display_layout.addWidget(self.text_display)
        
        # Create button layout
        button_layout = QHBoxLayout()
        
        # Create buttons
        self.load_btn = QPushButton("Load Image")
        self.scan_btn = QPushButton("Scan Document")
        self.extract_btn = QPushButton("Extract Text")
        self.save_btn = QPushButton("Save Results")
        
        # Style buttons
        for btn in [self.load_btn, self.scan_btn, self.extract_btn, self.save_btn]:
            btn.setMinimumHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border-radius: 5px;
                    padding: 5px 15px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:disabled {
                    background-color: #BDBDBD;
                }
            """)
        
        # Add buttons to layout
        button_layout.addWidget(self.load_btn)
        button_layout.addWidget(self.scan_btn)
        button_layout.addWidget(self.extract_btn)
        button_layout.addWidget(self.save_btn)
        
        # Connect button signals
        self.load_btn.clicked.connect(self.load_image)
        self.scan_btn.clicked.connect(self.scan_document)
        self.extract_btn.clicked.connect(self.extract_text)
        self.save_btn.clicked.connect(self.save_results)
        
        # Initially disable buttons
        self.scan_btn.setEnabled(False)
        self.extract_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        
        # Add layouts to main layout
        main_layout.addLayout(display_layout)
        main_layout.addLayout(button_layout)
        
        # Style the window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333333;
            }
            QScrollArea {
                border: 2px solid #BDBDBD;
                border-radius: 5px;
                background-color: white;
            }
        """)
        
    def create_display_section(self, title):
        section = QWidget()
        layout = QVBoxLayout(section)
        
        # Add title
        title_label = QLabel(title)
        layout.addWidget(title_label)
        
        # Create scroll area for image
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumSize(350, 600)
        
        # Create image label
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll.setWidget(image_label)
        
        layout.addWidget(scroll)
        
        # Store reference to image label
        setattr(self, f"{title.lower().replace(' ', '_')}_label", image_label)
        
        return section
    
    def create_text_section(self, title):
        section = QWidget()
        layout = QVBoxLayout(section)
        
        # Add title
        title_label = QLabel(title)
        layout.addWidget(title_label)
        
        # Create text edit
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setMinimumSize(350, 600)
        
        layout.addWidget(self.text_edit)
        
        return section
    
    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.tiff)")
        
        if file_path:
            self.original_image_path = file_path
            self.update_image_display(self.original_image_label, file_path)
            self.scan_btn.setEnabled(True)
            
            # Store the basename for later use
            self.current_basename = os.path.basename(file_path)
    
    def scan_document(self):
        if self.original_image_path:
            try:
                # Create the command
                command = [
                    sys.executable,
                    "scan.py",
                    "--image",
                    f"{self.original_image_path}",
                ]
                
                # Run the command
                process = subprocess.Popen(command)
                process.wait()  # Wait for the process to complete
                
                # Check if the scanned image exists
                self.scanned_image_path = os.path.join('output', self.current_basename)
                
                if os.path.exists(self.scanned_image_path):
                    self.update_image_display(self.scanned_image_label, self.scanned_image_path)
                    self.extract_btn.setEnabled(True)
                else:
                    QMessageBox.warning(self, "Error", "Scanned image not found in output directory.")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error during scanning: {str(e)}")
    
    def update_image_display(self, label, image_path):
        """Updates the image display to fit within the label while keeping the aspect ratio."""
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        label.setPixmap(scaled_pixmap)
    
    def resizeEvent(self, event):
        """Handle window resizing to adjust image displays."""
        if self.original_image_path:
            self.update_image_display(self.original_image_label, self.original_image_path)
        if self.scanned_image_path:
            self.update_image_display(self.scanned_image_label, self.scanned_image_path)
        super().resizeEvent(event)
    
    def extract_text(self):
        if self.scanned_image_path and os.path.exists(self.scanned_image_path):
            try:
                # Perform OCR
                results = self.reader.readtext(self.scanned_image_path)
                
                # Extract and display text
                extracted_text = "\n".join([text[1] for text in results])
                self.text_edit.setText(extracted_text)
                self.save_btn.setEnabled(True)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error during text extraction: {str(e)}")
    
    def save_results(self):
        if hasattr(self, 'text_edit') and self.text_edit.toPlainText():
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Text", "", "Text Files (*.txt)")
            
            if file_path:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(self.text_edit.toPlainText())
                    QMessageBox.information(self, "Success", "Text saved successfully!")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error saving file: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DocumentScannerGUI()
    window.show()
    sys.exit(app.exec())
