import React, {useState} from 'react';
import router from 'next/router';
import {Icon, PageHeader} from 'antd';

import {AppLayout} from '../../../components/AppLayout';

import OCRUpload from '../../../components/ocr/ocrUpload';
import {withRedux} from "../../../stores/redux";

const UploadPage = () => {
  return (
    <AppLayout>
      <PageHeader
        style={{
          border: '1px solid rgb(235, 237, 240)',
        }}
        backIcon={
          <Icon type="arrow-left"/>
        }
        onBack={() => router.push('/')}
        title="OCR Demo"
        subTitle="Upload image to try out Text Recognition."
      />
      <OCRUpload/>
    </AppLayout>
  );
}

export default withRedux(UploadPage)
