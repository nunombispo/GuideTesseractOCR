import cv2
import numpy as np
import pytesseract
from PIL import Image
from pdf2image import convert_from_path


# Convert PDF pages to images
pdf_path = 'catalog-german-multilingual.pdf'
pages = convert_from_path(pdf_path, 300)  # 300 is the resolution (dpi)

# Extract text from each page
extracted_text = ""

for page_number, page_image in enumerate(pages, start=1):
    # Perform OCR on the page image
    text = pytesseract.image_to_string(page_image, lang='deu')
    extracted_text += f"--- Page {page_number} ---\n"
    extracted_text += text + "\n"

# Print or process the extracted text
print(extracted_text)
