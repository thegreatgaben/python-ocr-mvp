import React, {useEffect, useState} from 'react';
import 'antd/dist/antd.css';
import {AppLayout} from '../components/AppLayout';
import {Layout, Row, Col, Card, Tag, Divider, Statistic, Icon} from "antd";
import style from './index.scss'

const Dashboard = () => {
  return (
    <AppLayout>
      <Row gutter={[16, 16]}>
        <Col className={style.col} md={24} lg={12} xl={8} xxl={8}>
          <Card className={style.gridCard}>
            <div className={style.spaceBetween}>
              <Statistic title="Artworks in Progress" value={12} prefix={<Icon theme="twoTone" type="picture" />} />
              <div>
                <Tag className={style.filterTag}>Right Now</Tag>
              </div>
            </div>
          </Card>
        </Col>
        <Col className={style.col} md={24} lg={12} xl={8} xxl={8}>
          <Card className={style.gridCard}>
            <div className={style.spaceBetween}>
              <Statistic title="Total Completed Artworks" value={1128} prefix={<Icon theme="twoTone" type="picture" />} />
              <div>
                <Tag className={style.filterTag}>This Year</Tag>
              </div>
            </div>
          </Card>
        </Col>
        <Col className={style.col} md={24} lg={12} xl={8} xxl={8}>
          <Card className={style.gridCard}>
            <div className={style.spaceBetween}>
              <Statistic title="Total Revenue Generated (MYR)" value={142324} precision={2} prefix={<Icon theme="twoTone" type="dollar" />} />
              <div>
                <Tag className={style.filterTag}>This Year</Tag>
              </div>
            </div>
          </Card>
        </Col>
        <Col className={style.col} sm={24} md={24}>
          <Card className={style.gridCard}>
            <div className={style.spaceBetween}>
              <Statistic title="Efficiency Rating" value={1086} prefix={<Icon theme="twoTone" type="dashboard" />} />
              <Tag className={style.filterTag}>This Year</Tag>
            </div>
            <Divider dashed />

              <Row gutter={[32, 32]}>
                <Col sm={24} md={24} lg={12} xxl={12}>
                  <Statistic title="Average Time Spent Per Artwork" value={'3h 26m'} prefix={<Icon theme="twoTone" type="hourglass" />} />
                </Col>
                <Col sm={24} md={24} lg={12} xxl={12}>
                  <Statistic title="Average Revenue Per Artwork (MYR)" value={6036} precision={2} prefix={<Icon theme="twoTone" type="money-collect" />} />
                </Col>
              </Row>
            <Divider dashed />

              <Row gutter={[32, 32]}>
                <Col sm={24} md={12} lg={8} xl={6}>
                  <Statistic title="Fonts Matched" value={724} prefix={<Icon theme="twoTone" type="eye" />} />
                </Col>
                <Col sm={24} md={12} lg={8} xl={6}>
                  <Statistic title="Images Vectorized" value={136} prefix={<Icon theme="twoTone" type="highlight" />} />
                </Col>
                <Col sm={24} md={12} lg={8} xl={6}>
                  <Statistic title="Images Color-Separated" value={281} prefix={<Icon theme="twoTone" type="picture"/>} />
                </Col>
                <Col sm={24} md={12} lg={8} xl={6}>
                  <Statistic title="Images Trapped" value={92} prefix={<Icon theme="twoTone" type="edit" />} />
                </Col>
              </Row>

          </Card>
        </Col>
      </Row>
    </AppLayout>
  );
}

export default Dashboard
