import React, { useState } from 'react';
import { Layout } from 'antd';
import style from './AppLayout.scss'
import { Sidebar } from './Sidebar';
import { Brand } from './Brand';
const { Content, Footer, Header, Sider } = Layout;

export function AppLayout(props) {

  const [collapsed, setCollapsed] = useState(false);

  const onCollapse = () => {
    setCollapsed(!collapsed);
  };

  return (
    <Layout>
      <Sider
        className={style.siderLeft}
        collapsible
        collapsed={collapsed}
        onCollapse={onCollapse}
        theme={'light'}
      >
        <Sidebar collapsed={collapsed}/>
      </Sider>
      <Sider
        className={style.fakeSider}
        collapsible
        collapsed={collapsed}
      >
      </Sider>
      <Layout
        className={style.layoutRight}
      >
        <Content className={style.content}>
          {props.children}
        </Content>
        <Footer className={style.footer}>Powered by Nixel</Footer>
      </Layout>
    </Layout>
  );
}
