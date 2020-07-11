import React, {useState} from 'react';
import {useSelector, useDispatch} from 'react-redux';
import * as _ from 'lodash';
import router from 'next/router';
import {http} from '../../services/axios';
import {Button, Descriptions, Form, Icon, message, Upload} from 'antd';

import {ImageDisplay} from '../ImageDisplay';
import {EmptyUpload} from '../EmptyUpload';

import {SET_COLOR_OUTPUTS, ApiResponse} from '../../typings/color-separation.d';

const useCSStore = () => {
  const colorOutputs = useSelector(state => state.csReducer.colorOutputs);
  const dispatch = useDispatch();
  const setOutputs = (newOutputs) => {
    dispatch({
      type: SET_COLOR_OUTPUTS,
      outputs: newOutputs,
    });
  };
  return { colorOutputs, setOutputs }
}

const CSUpload = () => {
  const [fields, setFields] = useState({
    file: undefined,
  });
  const hasFile = !!fields['file'];
  const originalImage = fields['file'];

  const [loading, setLoading] = useState(false);
  const [apiResponse, setApiResponse] = useState<ApiResponse>({});
  const baseURL = process.env.API_URL

  const { colorOutputs, setOutputs } = useCSStore();

  const uploadImage = async (values) => {
    const formData = new FormData();
    // append form data
    _.each(values, (value, key) => {
        formData.append(key, value)
    })

    setLoading(true);
    try {
        const response = await http.post<ApiResponse>('/api/v1/cs', formData);
        setApiResponse(() => response.data);
        setOutputs(response.data.layers);
    } catch (e) {
      console.log({e});
      message.error('Server Error!')
    } finally {
      setLoading(false);
    }
  }

  const handleFileInputChange = async (e) => {
    const fileInput = fields['file'];
    const isSameFile = fileInput && e.file && fileInput.name === e.file.name

    if (!isSameFile) {

      // clear previous responses
      setApiResponse({});

      // new image
      const newValues = ({
        ...fields,
        file: e.file.originFileObj
      })

      // update field value
      setFields(newValues)

      if (e.file) {
        uploadImage(newValues)
      }
    }
  }

  return (
    <div>
      <Upload.Dragger
        accept="image/*"
        onChange={handleFileInputChange}
        showUploadList={false}
        style={{ minHeight: '300px' }}
      >
        {hasFile ? (
          <ImageDisplay
            src={originalImage}
            alt="Original Image"
          />
        ) : <EmptyUpload/>}
      </Upload.Dragger>

      <div style={{
        marginTop: "10px",
      }}
      >
        {
          colorOutputs.map((output, index) => <ImageDisplay src={`${baseURL}/${output.filepath}`} key={index}/>)
        }
      </div>
    </div>
  )
}

export default CSUpload
