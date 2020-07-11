import React from 'react';
import {Menu, Icon} from 'antd';
import style from './Sidebar.scss'
import Link from 'next/link';
import {Brand} from "./Brand";

export function Sidebar(props) {

  return (
    <div>
      <div className={style.brand}>
        <Brand onlyLogo={props.collapsed}/>
      </div>
      <Menu className={style.sidebarMenu}>
        <div
          className={style.sidebarTitle}
          style={{textAlign: props.collapsed ? 'center' : 'left'}}
        >
          HOME
        </div>
        <Menu.Item key="1">
          <Icon type="desktop" />
          {!props.collapsed && 'Dashboard'}
          <Link href="/"><a>Dashboard</a></Link>
        </Menu.Item>
        <Menu.Item key="2">
          <Icon type="picture" />
          {!props.collapsed && 'Editor'}
          <Link href="/editor"><a>Editor</a></Link>
        </Menu.Item>
        <div
          className={style.sidebarTitle}
          style={{textAlign: props.collapsed ? 'center' : 'left'}}
        >
          TOOLS
        </div>
        <Menu.Item key="3">
          <Icon type="font-colors" />
          {!props.collapsed && 'Text Detection'}
          <Link href="/ocr/upload"><a>Text Detection</a></Link>
        </Menu.Item>
      </Menu>
    </div>
  );
}
