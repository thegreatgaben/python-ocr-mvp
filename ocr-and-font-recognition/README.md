# OCR and Font Recognition


## Prerequisites

1. Go get `conda` installed and install `environment.yml`
1. You need some training data.
2. Put them in `big_assets/tesseract/training_data`
3. You can find all the training data here: https://github.com/tesseract-ocr/tessdata_best
4. We're using the best version because accuracy is more important for us


# Environment management

1. All these commands must be run in the same folder as this `README.md`
1. To install the environment, run `conda env create -f environment.yml`
2. To activate an environment, run `conda activate nixel-ocr-and-font-recognition`
2. To update the environment.yml, run `conda env export | grep -v "prefix" > environment.yml`
3. To update your current environment, run `conda env update -f environment.yml --prune`

# How to run the tests?

1. Try something like `python -m tests.font_matching.font_matching`
