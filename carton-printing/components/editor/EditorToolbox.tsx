import React from 'react';
import style from './EditorToolbox.scss';
import {} from 'antd';

export function EditorToolbox(props) {
  return (
    <div className={style.toolbox}>
      {props.children}
    </div>
  );
}
