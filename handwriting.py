import cv2
import numpy as np
import pytesseract
from PIL import Image
from pdf2image import convert_from_path


# Function to preprocess the image for better OCR results
def preprocess_image(image):
    # Read the image using OpenCV
    img = cv2.imread(image)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply adaptive thresholding to binarize the image
    binary_img = cv2.adaptiveThreshold(blurred, 255,
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 2)

    # Deskew the image by calculating the rotation angle and rotating it back
    coords = np.column_stack(np.where(binary_img > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = binary_img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    deskewed_img = cv2.warpAffine(binary_img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # Save the preprocessed image for inspection
    cv2.imwrite('preprocessed_image.png', deskewed_img)

    return deskewed_img


# Convert PDF pages to images
pdf_path = 'Edsger-Dijkstra-Notes-handwriting.pdf'
pages = convert_from_path(pdf_path, 500)  # 500 is the resolution (dpi)

# Extract text from each page
extracted_text = ""

for page_number, page_image in enumerate(pages, start=1):
    # Save the page image to disk
    page_image.save(f'page_{page_number}.png', 'PNG')

    # Preprocess the image
    processed_image = preprocess_image(f'page_{page_number}.png')

    # Convert the processed image back to PIL format for Tesseract
    pil_img = Image.fromarray(processed_image)

    # Perform OCR on the page image
    text = pytesseract.image_to_string(page_image)
    extracted_text += f"--- Page {page_number} ---\n"
    extracted_text += text + "\n"

# Print or process the extracted text
print(extracted_text)
