import React from 'react';
import {useSelector, useDispatch} from 'react-redux';
import style from './PropertiesWindow.scss';
import {List, Avatar, Icon} from "antd";
import {Layer, UPDATE_LAYER, TOGGLE_LAYER_VISIBILITY} from '../../../typings/editor.d';


const useEditorStore = () => {
  const dispatch = useDispatch();
  const toggleLayerVisibility = (index, value) => {
    dispatch({
      type: TOGGLE_LAYER_VISIBILITY,
      layerIndex: index,
      visibility: !value
    })
  };
  return { toggleLayerVisibility };
}

const PropertiesWindow = () => {
  const layers: Layer[] = useSelector(state => state.editorReducer.layers);

  const { toggleLayerVisibility } = useEditorStore();

  return (
    <div className={style.properties}>
      <div className={style.propertyTitle}>Properties</div>
      <img className={style.colorPicker} src={'/static/editor/colorpicker.png'}/>
      <div className={style.propertyTitle}>Layers and Elements</div>
      <List
        className={style.layerList}
        itemLayout="horizontal"
        dataSource={layers}
        renderItem={(item, index) => (
          <List.Item className={style.layerItem}>
            <List.Item.Meta
              avatar={
                <Avatar
                  shape="square"
                  className={style.layerImage}
                  src={item.previewImg}
                />
              }
              title={item.title}
              description={item.type}
            />
            {
              item.visibility ?
                  <Icon
                    className={style.layerVisibilityIcon}
                    type="eye"
                    theme="filled"
                    onClick={() => toggleLayerVisibility(index, item.visibility)}
                  />
              :
                  <Icon
                    className={style.layerVisibilityIcon}
                    type="eye-invisible"
                    theme="filled"
                    onClick={() => toggleLayerVisibility(index, item.visibility)}
                  />
            }
            <img src={'/static/editor/dragger.svg'}/>
          </List.Item>
        )}
      />
    </div>
  )
}

export default PropertiesWindow;
