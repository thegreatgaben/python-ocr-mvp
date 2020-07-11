import React from 'react';
import {Select} from 'antd';
import {SelectProps} from 'antd/lib/select';

import {Languages} from '../typings/ocr';

interface LanguageProps extends SelectProps<Languages[]> {}

const defaultProps = {
  onChange() {},
  value: undefined,
}

export function LanguageSelection(props: LanguageProps = defaultProps) {
  return (
    <Select<Languages[]>
      defaultValue={['eng']}
      mode="multiple"
      value={props.value}
      style={props.style}
      onChange={props.onChange}
    >
      <Select.Option value="eng">English</Select.Option>
      <Select.Option value="chi_sim">Chinese Simplified</Select.Option>
      <Select.Option value="chi_tra">Chinese Traditional</Select.Option>
      <Select.Option value="khm">Khmer</Select.Option>
      <Select.Option value="tai">Thai</Select.Option>
      <Select.Option value="vie">Vietnamese</Select.Option>
    </Select>
  );
}
