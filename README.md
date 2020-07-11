# Python OCR MVP
This project was a minimum viable product, that aimed to help designers in the carton box printing industry to streamline their
work in a more efficient manner. We had an ambitious goal to make it an alternative web solution to Adobe Illustrator, 
that has tools specially made to benefit carton box printing designers. 
One such tool was to employ Optical Character Recognition (OCR) 
and Font matching, as well as Color Separation on an image. OCR and Color Separation was only implemented in this case. I worked on the OCR part, while one of my other colleague worked on Color Separation. Although the project did not went through
in the end, it was a good learning experience.


## Instructions for running this project
Ensure you have these installed beforehand:
- Python 3.8
- [Miniconda environment manager](https://docs.conda.io/en/latest/miniconda.html)
- [Flask micro web framework](https://flask.palletsprojects.com/en/1.1.x/installation/#installation)
- [Tesseract OCR Engine](https://github.com/tesseract-ocr/tesseract)
- [Yarn](https://classic.yarnpkg.com/en/docs/install/#debian-stable)

Once these are installed, refer to the `README.md` in `ocr-and-font-recognition/` folder to learn how to setup the Conda
environment with the necessary dependencies installed.

To run the backend server locally:
```
# Runs at localhost:5000
python app.py 
```

To run the frontend locally:
```
# Go to frontend folder
cp carton-printing/

# Install dependencies
yarn

# Set environment variables
cp .env.example .env

# Runs Next.js dev server at localhost:3000
yarn run dev
```

Example input images can be found in `ocr-and-font-recognition/test/input/`

