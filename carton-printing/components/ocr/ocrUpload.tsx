import React, {useState} from 'react';
import {useSelector, useDispatch} from 'react-redux';
import * as _ from 'lodash';
import router from 'next/router';
import {http} from '../../services/axios';
import {Button, Descriptions, Form, Icon, message, Upload, Progress} from 'antd';

import {ImageDisplay} from '../ImageDisplay';
import {EmptyUpload} from '../EmptyUpload';

import {setOCRList} from '../../utils/ocr';

import {Languages, TextObject, ApiResponse, SET_ORIGINAL_IMAGE_URL} from '../../typings/ocr.d';
import {LanguageSelection} from '../LanguageSelection';

import style from './ocrUpload.scss';

const FILE_INPUT = 'file'
const LANG_INPUT = 'lang'

function ImageCompare({originalImage, ocrImage}) {
  if (ocrImage) {
    return (
      <ImageDisplay
        src={ocrImage}
        alt="Image with Text Regions"
      />
    )
  } else {
    return (
      <ImageDisplay
        src={originalImage}
        alt="Original Image"
      />
    )
  }
}

const useOCRStore = () => {
  const recognisedTexts = useSelector(state => state.ocrReducer.recognisedTexts);
  const dispatch = useDispatch();
  const setTexts = (newTexts) => {
    dispatch({
      type: 'SET_TEXTS',
      texts: newTexts,
    });
  }
  const setOrigImgURL = (newURL) => {
    dispatch({
      type: SET_ORIGINAL_IMAGE_URL,
      url: newURL,
    });
  }
  return { recognisedTexts, setTexts, setOrigImgURL }
}

const OCRUpload = () => {
  const [fields, setFields] = useState({
    [FILE_INPUT]: undefined,
    [LANG_INPUT]: ['eng']
  });
  const hasFile = !!fields[FILE_INPUT];
  const originalImage = fields[FILE_INPUT];
  const langValue = fields[LANG_INPUT] as Languages[];
  const [loading, setLoading] = useState(false);
  const [apiResponse, setApiResponse] = useState<ApiResponse>({})
  const [ocredImageURL, setOcredImageURL] = useState(undefined);

  const { recognisedTexts, setTexts, setOrigImgURL } = useOCRStore();

  const [progress, setProgress] = useState(0);

  async function submitForm(values) {
    console.log(values);
    setLoading(true);
    const formData = new FormData();

    // append form data
    _.each(values, (value, key) => {
      if (key === 'lang') {
        const langValue = typeof value === 'string' ? value : value.join('+')
        formData.append(key, langValue)
      } else {
        formData.append(key, value)
      }
    })

    let updatedProgress = progress;
    const progressInterval = setInterval(() => {
      updatedProgress += 4;
      if (updatedProgress <= 100) {
        setProgress(updatedProgress)
      }
    }, 1000);

    try {
      const response = await http.post<ApiResponse>('/api/v1/ocr', formData);
      setApiResponse(() => response.data)
      const ocrImageURL = `${process.env.API_URL}/${response.data.textDetectionsURL}`

      setOrigImgURL(response.data.originalImageURL);
      setTexts(response.data.recognisedTexts);
      // update to localStorage
      setOCRList({
        name: response.data.filename,
        path: ocrImageURL,
        recognisedTexts: response.data.recognisedTexts,
        lang: fields[LANG_INPUT] as Languages[]
      });

      setOcredImageURL(ocrImageURL)
    } catch (e) {
      console.log({e});
      message.error('Server Error!')
    } finally {
      setLoading(false);
      clearInterval(progressInterval);
      setProgress(0);
    }
  }

  const handleOnChangeLanguage = async (value) => {
    setFields(fields => ({
      ...fields,
      [LANG_INPUT]: value
    }))
  }

  const handleFileInputChange = async (e) => {
    const fileInput = fields[FILE_INPUT];
    const isSameFile = fileInput && e.file && fileInput.name === e.file.name

    if (!isSameFile) {

      // clear previous responses
      setApiResponse({});
      setOcredImageURL(undefined);

      // new image
      const newValues = ({
        ...fields,
        [FILE_INPUT]: e.file.originFileObj
      })

      // update field value
      setFields(newValues)

      if (e.file) {
        await submitForm(newValues);
      }
    }
  }

  return (
    <div className={style.home}>
      <div className={style.homeContent}>
        <Form
          onSubmit={(e) => {
            e.preventDefault();
            // noinspection JSIgnoredPromiseFromCall
            submitForm(fields);
          }}
        >
          {
            loading &&
            <Progress percent={progress} status="active"/>
          }
          <Form.Item label="Languages">
            <LanguageSelection
              onChange={handleOnChangeLanguage}
              value={langValue}
            />
            <Button
              type="primary"
              htmlType="submit"
            >
              Submit
            </Button>
          </Form.Item>
          <Upload.Dragger
            className={style.homeUpload}
            accept="image/*"
            onChange={handleFileInputChange}
            showUploadList={false}
            style={{ minHeight: '300px' }}
          >
            {hasFile ? (
              <ImageCompare
                originalImage={originalImage}
                ocrImage={ocredImageURL}
              />
            ) : <EmptyUpload/>}
          </Upload.Dragger>
        </Form>
      </div>
      { recognisedTexts.length > 0 && (
        <Descriptions
          className={style.recognisedText}
          title="Recognised Texts"
        >
          {recognisedTexts.map((payload, index) => (
            <Descriptions.Item key={index}>{payload.text}</Descriptions.Item>
          ))}
        </Descriptions>
      )}
    </div>
  )
}

export default OCRUpload;
