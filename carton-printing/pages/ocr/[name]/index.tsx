import React, {useEffect, useState} from 'react';
import * as _ from 'lodash';
import {useRouter} from 'next/router';
import {Button, Descriptions, Form, Icon, PageHeader, Upload} from 'antd';

import {AppLayout} from '../../../components/AppLayout';
import {ImageDisplay} from '../../../components/ImageDisplay';
import {OCRObject} from '../../../typings/ocr';

import style from './ocrDetails.scss';
import {getOCRList} from '../../../utils/ocr';
import {LanguageSelection} from '../../../components/LanguageSelection';
import Link from 'next/link';

const OcrDetails = () => {
  const router = useRouter()
  const { name } = router.query
  const [ocrDetails, setOcrDetails] = useState<OCRObject>(undefined);
  const ocrName = _.get(ocrDetails, 'name', '');
  const ocredImageURL = _.get(ocrDetails, 'path', '');
  const recognisedTexts = _.get(ocrDetails, 'recognisedTexts', []) as string[];
  const langValue = _.get(ocrDetails, 'lang', []);

  useEffect(() => {
    const list = getOCRList()
    const item = list.find(item => item.name === name)

    setOcrDetails(item)
  }, [name]);

  return (
    <AppLayout>
      <div className={style.home}>
        <PageHeader
          style={{
            border: '1px solid rgb(235, 237, 240)',
          }}
          backIcon={
            <Icon type="arrow-left" />
          }
          onBack={() => router.push('/')}
          title={ocrName}
          subTitle="OCR & Text Recognition."
        />
        <div className={style.homeContent}>
          <Form
            labelCol={{span: 4}}
            onSubmit={(e) => {
              e.preventDefault();
              return false
            }}
          >
            <Form.Item label="Languages">
              <LanguageSelection
                value={langValue}
                disabled={true}
              />
              <Link
                href="../../ocr/upload"
              >
                <Button
                  type="primary"
                  htmlType="submit"
                  style={{marginLeft: 15}}
                >
                  Try a new one
                </Button>
              </Link>
            </Form.Item>
            <Upload.Dragger
              className={style.homeUpload}
              accept="image/*"
              showUploadList={false}
              disabled={true}
            >
              <ImageDisplay
                src={ocredImageURL}
                alt="Image with Text Regions"
              />
            </Upload.Dragger>
          </Form>
        </div>
        {recognisedTexts.length > 0 && (
          <Descriptions
            className={style.recognisedText}
            title="Recognised Texts"
          >
            {recognisedTexts.map((text, index) => (
              <Descriptions.Item key={index}>{text}</Descriptions.Item>
            ))}
          </Descriptions>
        )}
      </div>
    </AppLayout>
  );
}

export default OcrDetails
