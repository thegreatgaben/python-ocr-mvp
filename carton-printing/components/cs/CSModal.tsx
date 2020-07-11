import React from 'react';

import CSUpload from './csUpload';
import DesignToolModal from '../../components/DesignToolModal';

const CSModal = (props) => {
  const csTitle = "Color Separation Tool";

  const handleCSOk = () => {
    props.visibilityHandler();
  }
  const handleCSCancel = () => {
    props.visibilityHandler();
  }

  return (
    <DesignToolModal
      title={csTitle}
      visible={props.visible}
      submitHandler={handleCSOk}
      cancelHandler={handleCSCancel}
    >
        <CSUpload/>
    </DesignToolModal>
  );
}

export default CSModal;
