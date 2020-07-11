import React from 'react';

import OCRUpload from './ocrUpload';
import DesignToolModal from '../../components/DesignToolModal';

const OCRModal = (props) => {
  const ocrTitle = "OCR and Font Detection Tool";

  const handleOCROk = () => {
    props.visibilityHandler();
  }
  const handleOCRCancel = () => {
    props.visibilityHandler();
  }

  return (
    <DesignToolModal
      title={ocrTitle}
      visible={props.visible}
      submitHandler={handleOCROk}
      cancelHandler={handleOCRCancel}
    >
        <OCRUpload/>
    </DesignToolModal>
  );
}

export default OCRModal;
