import fitz
import easyocr
import os

from streamlit import text

reader = easyocr.Reader(['en'])

def analyze_report(file_path):

    text = ""

    # PDF
    if file_path.lower().endswith(".pdf"):

        pdf = fitz.open(file_path)

        for page in pdf:

            pix = page.get_pixmap()

            image_path = "temp_page.png"

            pix.save(image_path)

            result = reader.readtext(image_path, detail=0)

            text += "\n".join(result)

        pdf.close()

        if os.path.exists(image_path):
            os.remove(image_path)

    # Image
    else:

        result = reader.readtext(file_path, detail=0)

        text = "\n".join(result)

    text = text.lower()

    findings = []

    if "multiple cyst" in text:
        findings.append("Multiple ovarian cysts detected")

    if "polycystic" in text:
        findings.append("Polycystic ovary mentioned")

    if "cystic changes" in text:
        findings.append("Cystic changes found")

    if "bulky ovary" in text:
        findings.append("Bulky ovary")

    if "enlarged ovary" in text:
        findings.append("Enlarged ovary")

    score = len(findings)

    if score >= 3:
        confidence = 95
    elif score == 2:
        confidence = 85
    elif score == 1:
        confidence = 70
    else:
        confidence = 20

    positive = confidence >= 80

    return positive, confidence, findings, text
