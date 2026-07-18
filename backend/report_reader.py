import fitz
import easyocr
import cv2
import os

reader = easyocr.Reader(['en'])

def read_report(file_path):

    text = ""

    extension = os.path.splitext(file_path)[1].lower()

    # ---------- PDF ----------

    if extension == ".pdf":

        pdf = fitz.open(file_path)

        for page in pdf:

            pix = page.get_pixmap()

            image_path = "temp/page.png"

            pix.save(image_path)

            result = reader.readtext(image_path, detail=0)

            text += "\n".join(result)

        pdf.close()

    # ---------- Image ----------

    else:

        image = cv2.imread(file_path)

        result = reader.readtext(image, detail=0)

        text = "\n".join(result)

    return text