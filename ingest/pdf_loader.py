from pypdfium2 import PdfDocument
from PIL import Image
import numpy as np

def pdf_to_images(pdf_path: str) -> list:
    with PdfDocument(pdf_path) as pdf:
        images = []
        for page_num in range(len(pdf)):
            pil_img = pdf[page_num].to_pil()
            images.append(np.array(pil_img))  # Converte para formato np.array(BGR)
    return images