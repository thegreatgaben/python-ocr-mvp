import React, {useEffect, useState} from 'react';
import 'antd/dist/antd.css';

import {AppLayout} from '../../components/AppLayout';
import CSUpload from "../../components/cs/csUpload";
import {Icon, PageHeader} from "antd";
import router from "next/dist/client/router";
import {withRedux} from "../../stores/redux";

const ColorSeparationUpload = () => {
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
        title="Color Separation"
        subTitle="Upload image to try out Color Separation. (More parameters to come!)"
      />
      <CSUpload/>
    </AppLayout>
  );
}

export default withRedux(ColorSeparationUpload)
