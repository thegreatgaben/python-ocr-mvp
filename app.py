from flask import *
import io
import numpy as np
import cv2 as cv
import random


# Path to your python modules
import sys
sys.path.append("./color-separation/")
sys.path.append("./ocr-and-font-recognition/")

from mser_text_detection import MSERTextDetection
from ColorSeparation import ColorSeparationEngine
from ocr import OCREngine

app = Flask(__name__)
app.config["ALLOWED_EXTENSIONS"] = set(['png', 'jpg', 'jpeg'])

global ocrEngine, textDetector, csEngine

def main():
    # All things global should be defined here
    global ocrEngine, textDetector, csEngine
    textDetector = MSERTextDetection()
    ocrEngine = OCREngine(padding=True, roiPadding=0.025)
    csEngine = ColorSeparationEngine()


def valid_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config["ALLOWED_EXTENSIONS"]


def handle_file_upload(request):
    # check if the post request has the file part
    if 'file' not in request.files:
        print('No file part')
        return (np.array([]), '')

    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        print('No selected file')
        return (np.array([]), file.filename)

    if file and valid_file(file.filename):
        return (decode_img(file), file.filename)


def decode_img(file):
    in_memory_img = io.BytesIO()
    file.save(in_memory_img)
    imgbuf = np.fromstring(in_memory_img.getvalue(), np.uint8)
    img = cv.imdecode(imgbuf, cv.IMREAD_UNCHANGED)
    return img


def createErrorResponse(message, code):
    payload = {}
    payload["error_message"] = message
    payload["http_code"] = code
    return jsonify(payload), code


@app.route("/")
def hello_world():
    return "Nothing to see here... :D"


@app.errorhandler(404)
def not_found(error):
    return "404 NOT FOUND!", 404


@app.errorhandler(405)
def method_not_allowed(error):
    return "405 METHOD NOT ALLOWED", 405


@app.route("/api/v1/ocr", methods=["POST"])
def ocr_endpoint():
    image, filename = handle_file_upload(request)
    if image.shape[0] == 0:
        return createErrorResponse("NO IMAGE UPLOADED", 400)

    # For a grayscale/single channel image that is uploaded
    if len(image.shape) == 2:
        image = cv.merge((image, image, image))

    languages = request.form.get("lang")
    if languages is None:
        return createErrorResponse("NO LANGUAGE(S) SPECIFIED", 400)

    (imageHeight, imageWidth) = image.shape[:2]
    imageMeta = {}
    imageMeta["ext"] = filename.split('.')[1]
    imageMeta["width"] = imageWidth
    imageMeta["height"] = imageHeight
    imageMeta["filename"] = filename

    outputFileName = "{}_{}_texts".format(filename.split('.')[0], languages)
    outputFileNameWithExt = outputFileName + '.' + imageMeta["ext"]

    boxes = textDetector.detectTexts(image, imageMeta, outputFileNameWithExt)
    results = ocrEngine.performOCR(image, boxes, imageMeta, languages)

    payload = {}
    payload["recognised_texts"] = results
    payload["filename"] = outputFileName
    payload["textDetectionsURL"] = textDetector.getOutputFilePath(
        outputFileNameWithExt)
    response = jsonify(payload)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200


@app.route("/api/v1/cs", methods=["POST"])
def color_separation_endpoint():
    image, filename = handle_file_upload(request)
    if image.shape[0] == 0:
        return createErrorResponse("NO IMAGE UPLOADED", 400)

    outpath = 'color-separation/outputs'
    csEngine.clearFolder(outpath)
    csEngine.images = [image]
    csEngine.colorBalance(10)
    csEngine.blur(4)
    csEngine.otsuThreshMultiRGB(2)
    csEngine.writeOutput(outpath)
    imagePaths = csEngine.getImagePaths(outpath)

    payload = {}
    payload["filenames"] = imagePaths
    response = jsonify(payload)
    print('response haha: ' + str(response))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200


if __name__ == "__main__":
    main()
    app.run()
