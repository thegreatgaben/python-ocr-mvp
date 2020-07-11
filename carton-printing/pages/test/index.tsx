import React, {useEffect, useState} from 'react';
import {Button} from 'antd';

import {AppLayout} from '../../components/AppLayout';

import OCRModal from '../../components/ocr/OCRModal';
import CSModal from '../../components/cs/CSModal';

import style from './test.scss';


const TestModal = () => {
  const [ocrVisible, setOCRVisible] = useState(false);

  const [csVisible, setCSVisible] = useState(false);
  const csVisibilityHandler = () => {
    setCSVisible(!csVisible);
  };

  return (
    <AppLayout>
      <Button type="primary" onClick={() => setOCRVisible(!ocrVisible)}>
        OCR
      </Button>
      <OCRModal
        visible={ocrVisible}
        visibilityHandler={() => setOCRVisible(!ocrVisible)}
      />

      <Button type="primary" onClick={csVisibilityHandler}>
        Color Separation
      </Button>
      <CSModal
        visible={csVisible}
        visibilityHandler={csVisibilityHandler}
      />
    </AppLayout>
  )
}

export default TestModal
