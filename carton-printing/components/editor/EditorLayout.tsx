import 'antd/dist/antd.css';
import React, {useState} from 'react';
import { Layout as AntLayout, Dropdown, Button, Icon, Menu } from 'antd';
const { Content, Header } = AntLayout;
import { Brand } from '../Brand';
import Link from "next/link";
import { GridButton } from './GridButton';
import style from './EditorLayout.scss'

import OCRModal from '../../components/ocr/OCRModal';
import CSModal from '../../components/cs/CSModal';


export function EditorLayout(props) {
  const [ocrVisible, setOCRVisible] = useState(false);
  const [csVisible, setCSVisible] = useState(false);

  const handleMenuClick = (e) => {
    console.log('click', e);
  };

  const handleOCRClick = () => {
    setOCRVisible(true);
  };

  const handleCSClick = () => {
    setCSVisible(true);
  };

  const menu = (
      <div className={style.dropdownMenu}>
        <Menu
          className={style.menuList}
          onClick={handleMenuClick}
        >
          <Menu.Item key="1">Save as..</Menu.Item>
          <Menu.Item key="2">Import</Menu.Item>
          <Menu.Item key="3">Export</Menu.Item>
          <Menu.Item key="4">Toggle Fullscreen</Menu.Item>
          <Menu.Item key="5">
            Quit
            <Link href="/"><a>Quit</a></Link>
          </Menu.Item>
        </Menu>
        <div className={style.menuGrid}>
          <GridButton
            onClick={handleOCRClick}
            title={'OCR and Font Detection'}
            subtitle={'Automatically recognise texts, detect font family and styles'}
            imgSrc={'/static/ocr.svg'}
            imgBgColor={'#91AAFC'}
          />
        </div>
      </div>
  );

  return (
    <AntLayout className={style.layout}>
      <Header className={style.header}>
        <Dropdown
          overlay={menu}
          overlayClassName={style.dropdownContainer}
        >
          <Button className={style.menuClickable}>
            <Brand subtext={'editor'}/>
            <Icon type="down" />
          </Button>
        </Dropdown>
        <div className={style.spacer}/>
        <Button type='danger' className={style.headerButton}>
          <Link href={'/'}>
            <a>Quit</a>
          </Link>
        </Button>
      </Header>
      <Content className={style.content}>
        <OCRModal
          visible={ocrVisible}
          visibilityHandler={() => setOCRVisible(!ocrVisible)}
        />
        <CSModal
          visible={csVisible}
          visibilityHandler={() => setCSVisible(!csVisible)}
        />
        {props.children}
      </Content>
    </AntLayout>
  );
}
