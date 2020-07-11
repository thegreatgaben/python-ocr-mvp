export type Languages = 'eng' | 'chi_sim' | 'chi_tra' | 'khm' | 'vie';

export interface TextObject {
  top: number;
  left: number;
  ratioTop: number;
  ratioLeft: number;
  text: string;
  fontFamily: string;
  fontSize: number;
}

export interface OCRObject {
  name: string;
  path: string;
  recognisedTexts: TextObject[];
  lang: Languages[];
}

export interface ApiResponse {
  recognisedTexts?: TextObject[];
  originalImageURL?: string;
  textDetectionsURL?: string;
  filename?: string;
}

export interface OCRState {
  originalImageURL: string;
  recognisedTexts: TextObject[];
}

// Action Types
export const SET_TEXTS = 'SET_TEXTS';
export type SET_TEXTS = typeof SET_TEXTS;
export interface SetTexts {
  type: SET_TEXTS;
  texts: TextObject[];
}

export const SET_ORIGINAL_IMAGE_URL = 'SET_ORIGINAL_IMAGE_URL';
export type SET_ORIGINAL_IMAGE_URL = typeof SET_ORIGINAL_IMAGE_URL;
export interface SetOriginalImageURL {
  type: SET_ORIGINAL_IMAGE_URL;
  url: string;
}

export type OCRActions = SetTexts | SetOriginalImageURL;


