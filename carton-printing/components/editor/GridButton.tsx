import React from 'react';
import style from './GridButton.scss';
import { Button } from 'antd';

export function GridButton(props) {
  return (
    <Button
      onClick={props.onClick}
      className={style.gridButton}
      style={{backgroundColor: props.bgColor}}
    >
      <img
        className={style.gridImg}
        style={{backgroundColor: props.imgBgColor}}
        src={props.imgSrc}
      />
      <div className={style.gridText}>
        <span className={style.title}>{props.title}</span>
        <span className={style.subtitle}>{props.subtitle}</span>
      </div>
    </Button>
  );
}
