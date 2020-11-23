import PIL.Image
import pytesseract
from wand.image import Image as wi

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

PDFfile = wi(filename="pdfTest/tutelaTest.pdf",resolution=300)
Images = PDFfile.convert('jpg')
ImageSequence = 1

for img in PDFfile.sequence:
    Image = wi(image = img)
    Image.save(filename="Image"+str(ImageSequence)+".jpg")
    print(ImageSequence)
    ImageSequence += 1

filelimit = ImageSequence-1

outfile = "out_text.txt"

f = open(outfile, "a", encoding='utf-8')

# Iterate from 1 to total number of pages
for i in range(1, filelimit + 1):
    filename = "image" + str(i) + ".jpg"

    text = str(((pytesseract.image_to_string(PIL.Image.open(filename)))))
    text = text.replace('-\n', '')
    print(i)
    f.write(text)

f.close()
