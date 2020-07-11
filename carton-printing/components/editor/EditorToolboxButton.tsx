import React from 'react';
import style from './EditorToolboxButton.scss';

export function EditorToolboxButton(props) {
  return (
    <div className={style.toolboxIcon}>
      {props.children}
    </div>
  );
}
