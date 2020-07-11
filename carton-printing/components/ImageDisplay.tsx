import React, {useState} from 'react';
import {readFileAsURL} from '../utils/image';
import {Card} from 'antd';
import style from './ImageDisplay.scss';

export const ImageDisplay = (props) => {
  const [imgURL, setImgURL] = useState();
  if (!props.loading) {
    if (props.src && props.src instanceof File) {
      readFileAsURL(props.src, setImgURL);
    } else {
      if (imgURL !== props.src) {
        setImgURL(props.src);
      }
    }
  }

  return <>
    <Card
      className={style.imageDisplay}
      loading={props.loading}
    >
      {props.src &&<div className="ant-card-cover">
        <img src={imgURL || props.src} alt={props.alt || 'Image'}/>
      </div>}
      <Card.Meta
        title={props.alt}
        description=""
      />
    </Card>
  </>;
};
