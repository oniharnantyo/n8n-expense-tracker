from flask import Flask, request, jsonify
from PIL import Image
from pdf2image import convert_from_bytes
import pytesseract

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    print(request.form)
    if 'file' not in request.files:
        return jsonify(
            error={
                'file': 'This field is required.'
            }
        ), 400

    file = request.files['file']

    fileType = request.form.get('fileType')
    match fileType:
        case 'pdf':
            return pdf_to_text(file)
        case 'image':
            return image_to_text(file)
        case _:
            return jsonify(
                error={
                    'fileType': 'This field is required.'
                }
            ), 400

def pdf_to_text(file):
    images = convert_from_bytes(file.read())

    result = ""
    for i in range(len(images)):
        imageText = pytesseract.image_to_string(images[i], lang='ind')
        result += imageText + "\n"

    return jsonify({'result': result})    

def image_to_text(file):
    image = Image.open(file)
    image_text = pytesseract.image_to_string(image, lang='ind')

    return jsonify({'result': image_text})
    