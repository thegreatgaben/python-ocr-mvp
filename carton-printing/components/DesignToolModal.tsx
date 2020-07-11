import React, {useEffect, useState} from 'react';
import {Modal} from 'antd';

const DesignToolModal = (props) => {
  return (
    <Modal
      title={props.title}
      visible={props.visible}
      onOk={props.submitHandler}
      onCancel={props.cancelHandler}
      centered
      width="80%"
      style={{
        padding: "20px",
      }}
    >
      {props.children}
    </Modal>
  )
}

export default DesignToolModal;
