import {OCRState, OCRActions, SET_TEXTS, SET_ORIGINAL_IMAGE_URL} from '../typings/ocr.d';

export const ocrInitialState: OCRState = {
  originalImageURL: '',
  recognisedTexts: []
}

export const ocrReducer = (
  state: OCRState = ocrInitialState,
  action: OCRActions
): OCRState => {
  switch (action.type) {
    case SET_TEXTS:
      return {
        ...state,
        recognisedTexts: action.texts
      };
    case SET_ORIGINAL_IMAGE_URL:
      return {
        ...state,
        originalImageURL: action.url
      };
    default:
      return state;
  }
}
