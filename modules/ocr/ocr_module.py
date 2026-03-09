import cv2
import pytesseract
import os

# Tesseract path (update this if Tesseract is installed in a different location)
# Example default installation path on Windows:
# C:\Program Files\Tesseract-OCR\tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Resolve paths relative to this script so it works no matter the current working directory.
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
image_folder = os.path.join(root_dir, "requirments", "dataset", "images")
output_file = os.path.join(root_dir, "output", "extracted_text.txt")

all_text = ""

for image in os.listdir(image_folder):

    image_path = os.path.join(image_folder, image)

    img = cv2.imread(image_path)

    if img is None:
        continue

    # Preprocessing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    # OCR
    text = pytesseract.image_to_string(thresh)

    all_text += f"\n\n----- {image} -----\n"
    all_text += text

# Save result
with open(output_file,"w",encoding="utf-8") as f:
    f.write(all_text)

print("OCR Extraction Completed")