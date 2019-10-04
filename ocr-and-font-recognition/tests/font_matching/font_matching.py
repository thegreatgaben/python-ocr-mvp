import os

from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import argparse
import cv2
from pathlib import Path


root_dir = Path('../..').resolve()

def process():
    files = [f for f in os.listdir(Path('input/roman')) if f.suffix is not '']

    # pytesseract.image_to_string()