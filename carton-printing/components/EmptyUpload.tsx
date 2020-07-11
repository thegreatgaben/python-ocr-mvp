import {Empty} from 'antd';
import React from 'react';

export const EmptyUpload = () => {
  return <>
    <Empty
      image="../static/empty.png"
      imageStyle={{
        height: 60,
      }}
      description=""
    >
    </Empty>
    <p style={{marginTop: 15}}>Click or drag file to this area to upload</p>
  </>;
};
