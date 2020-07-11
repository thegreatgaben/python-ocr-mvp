import 'antd/dist/antd.css';
import { EditorLayout } from '../../components/editor/EditorLayout';
import React from 'react';
import style from './editor.scss';
import EditorCanvas from "../../components/editor/EditorCanvas";
import PropertiesWindow from "../../components/editor/properties/PropertiesWindow";
import {EditorToolbox} from "../../components/editor/EditorToolbox";
import {EditorToolboxButton} from "../../components/editor/EditorToolboxButton";
import {withRedux} from '../../stores/redux';

const EditorPage = () => {
  return (
    <EditorLayout>
      <div className={style.workspace}>
        <EditorCanvas/>
        <EditorToolbox>
          <EditorToolboxButton><img src={'/static/editor/toolbox/cursor.svg'} /></EditorToolboxButton>
          <EditorToolboxButton><img src={'/static/editor/toolbox/marquee.svg'} /></EditorToolboxButton>
          <EditorToolboxButton><img src={'/static/editor/toolbox/wand.svg'} /></EditorToolboxButton>
          <EditorToolboxButton><img src={'/static/editor/toolbox/perspective.svg'} /></EditorToolboxButton>
          <EditorToolboxButton><img src={'/static/editor/toolbox/move.svg'} /></EditorToolboxButton>
          <EditorToolboxButton><img src={'/static/editor/toolbox/text.svg'} /></EditorToolboxButton>
          <EditorToolboxButton><img src={'/static/editor/toolbox/rectangle.svg'} /></EditorToolboxButton>
          <EditorToolboxButton><img src={'/static/editor/toolbox/circle.svg'} /></EditorToolboxButton>
        </EditorToolbox>
        <PropertiesWindow/>
      </div>
    </EditorLayout>
  );
}

export default withRedux(EditorPage)
