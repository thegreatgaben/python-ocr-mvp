import {OCRObject} from '../typings/ocr';
import * as _ from 'lodash';

const OCR_KEY = 'ocr-list';

export function getOCRList(): OCRObject[] {
  return JSON.parse(localStorage.getItem(OCR_KEY)) as OCRObject[];
}

export function setOCRList(item: OCRObject) {
  const exitingList = getOCRList()
  const newList = [
    ...(_.isEmpty(exitingList) ? [] : exitingList),
    item,
  ]
  return localStorage.setItem(OCR_KEY, JSON.stringify(newList));
}
