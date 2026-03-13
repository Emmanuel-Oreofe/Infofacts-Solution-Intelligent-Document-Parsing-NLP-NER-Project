import pytesseract
from pdf2image import convert_from_path
from PIL import Image


def run_ocr(file_path):

    images = convert_from_path(file_path)

    extracted_text = ""

    for image in images:
        text = pytesseract.image_to_string(image)
        extracted_text += text + "\n"

    return extracted_text