import React from 'react';
import style from './Brand.scss'

export function Brand(props) {

  return (
    <div className={style.brand}>
      <img src="/static/box-logo.png" className={style.logo}/>
      {!props.onlyLogo &&
        <div className={style.textContainer}>
          <div className={style.brandText}>
            shibumi
          </div>
          {props.subtext &&
            <div className={style.subtext}>{props.subtext}</div>
          }
        </div>
      }
    </div>
  );
}
