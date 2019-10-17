import io
import numpy as np
import cv2 as cv
import random
from flask import *

# Path to your python modules
import sys
sys.path.append("./color-separation/");
sys.path.append("./ocr-and-font-recognition/");

from mser_text_detection import MSERTextDetection
from ocr import OCREngine


global ocrEngine, textDetector;
app = Flask(__name__);
app.config["ALLOWED_EXTENSIONS"] = set(['png', 'jpg', 'jpeg']);


def main():
    # All things global should be defined here
    global ocrEngine, textDetector;
    textDetector = MSERTextDetection();
    ocrEngine = OCREngine("eng", padding=True, roiPadding=0.025);


def valid_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in app.config["ALLOWED_EXTENSIONS"];


def handle_file_upload(request):
    # check if the post request has the file part
    if 'file' not in request.files:
        print('No file part')
        return (np.array([]), '');

    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        print('No selected file')
        return (np.array([]), file.filename);

    if file and valid_file(file.filename):
        return (decode_img(file), file.filename);


def decode_img(file):
    in_memory_img = io.BytesIO();
    file.save(in_memory_img);
    imgbuf = np.fromstring(in_memory_img.getvalue(), np.uint8);
    img = cv.imdecode(imgbuf, cv.IMREAD_UNCHANGED);
    return img;


@app.route("/")
def hello_world():
    return "Nothing to see here... :D";


@app.errorhandler(404)
def not_found(error):
    return "404 NOT FOUND!", 404;


@app.errorhandler(405)
def method_not_allowed(error):
    return "405 METHOD NOT ALLOWED", 405


@app.route("/api/v1/ocr", methods=["POST"])
def ocr_endpoint():
    image, filename = handle_file_upload(request);
    if image.shape[0] == 0:
        return "400 BAD REQUEST", 400;

    (imageHeight, imageWidth) = image.shape[:2];
    imageMeta = {};
    imageMeta["ext"] = filename.split('.')[1];
    imageMeta["width"] = imageWidth;
    imageMeta["height"] = imageHeight;

    boxes = textDetector.detectTexts(image, imageMeta);
    results = ocrEngine.performOCR(image, boxes, imageMeta);

    payload = {};
    payload["recognised_texts"] = results;
    payload["textDetectionsURL"] = textDetector.getOutputFilePath(imageMeta["ext"]);
    response = jsonify(payload);
    response.headers.add('Access-Control-Allow-Origin', '*');
    return response, 200;


if __name__ == "__main__":
    main();
    app.run();

