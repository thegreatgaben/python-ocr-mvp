import React, {useState, useEffect, useRef} from 'react';
import {useSelector, useDispatch} from 'react-redux';
import style from './EditorCanvas.scss';
import {fabric} from 'fabric';
import uuidv4 from 'uuid/v4';

import {Layer, FabricObjects, SET_CANVAS, ADD_CANVAS_OBJECTS, UPDATE_LAYER, ADD_LAYER} from '../../typings/editor.d';
import {ColorOutputObject} from '../../typings/color-separation.d';

const useEditorStore = () => {
  const dispatch = useDispatch();
  const editorCanvas = useSelector(state => state.editorReducer.editorCanvas);
  const layers = useSelector(state => state.editorReducer.layers);
  const setCanvas = (newCanvas) => {
    dispatch({
      type: SET_CANVAS,
      canvas: newCanvas,
    })
  };
  const addCanvasObjects = (canvasObjects: FabricObjects) => {
    dispatch({
      type: ADD_CANVAS_OBJECTS,
      objects: canvasObjects,
    })
  };
  const addLayer = (newLayer: Layer) => {
    dispatch({
      type: ADD_LAYER,
      layer: newLayer,
    });
  };
  const updateLayer = (index: number, keyToModify: string, newVal: any) => {
    dispatch({
      type: UPDATE_LAYER,
      layerIndex: index,
      key: keyToModify,
      value: newVal,
    });
  };
  return { editorCanvas, layers, setCanvas, addCanvasObjects, addLayer, updateLayer };
}

const EditorCanvas = () => {
  const baseURL = process.env.API_URL
  const editorCanvasId = 'editor-canvas';
  const canvasElem = useRef(undefined);

  const { editorCanvas, layers, setCanvas, addCanvasObjects, addLayer, updateLayer } = useEditorStore();

  const ocrImageURL = useSelector(state => state.ocrReducer.originalImageURL);
  const recognisedTexts = useSelector(state => state.ocrReducer.recognisedTexts);
  const colorOutputs = useSelector(state => state.csReducer.colorOutputs);

  // Component mounted
  useEffect(() => {
    const canvas = new fabric.Canvas(editorCanvasId, {
      width: canvasElem.current.clientWidth,
      height: canvasElem.current.clientHeight,
      // Indicates whether objects should remain in current stack position when selected
      preserveObjectStacking: true,
    });
    setCanvas(canvas);
  }, []);

  // Canvas Initialized
  useEffect(() => {
    if (editorCanvas) {
      const rectWidth = Math.round(editorCanvas.width * 3/4);
      const rectHeight = editorCanvas.height - 25;

      // create a blank artboard
      const artBoard = new fabric.Rect({
        left: editorCanvas.width/8,
        top: 10,
        fill: 'white',
        width: rectWidth,
        height: rectHeight
      });
      artBoard.selectable = false;
      editorCanvas.add(artBoard);
      const uuid = uuidv4();
      addCanvasObjects({ [uuid]: artBoard });
      updateLayer(0, 'objectKeys', [uuid]);

      document.onkeypress = (event) => {
        if (event.code === 'Delete') {
          editorCanvas.remove(editorCanvas.getActiveObject());
        }
      }

      editorCanvas.on('object:selected', (param) => {
        // console.log('selected', param.target);
      });

      editorCanvas.on('object:removed', (param) => {
        // console.log('removed', editorCanvas.getObjects().indexOf(param.target));
      });


      // Enable Panning of Canvas
      editorCanvas.on('mouse:down', function(opt) {
        let evt = opt.e;
        if (evt.altKey === true) {
          this.isDragging = true;
          this.selection = false;
          this.lastPosX = evt.clientX;
          this.lastPosY = evt.clientY;
        }
      });
      editorCanvas.on('mouse:move', function(opt) {
        if (this.isDragging) {
          let e = opt.e;
          this.viewportTransform[4] += e.clientX - this.lastPosX;
          this.viewportTransform[5] += e.clientY - this.lastPosY;
          this.requestRenderAll();
          this.lastPosX = e.clientX;
          this.lastPosY = e.clientY;
        }
      });
      editorCanvas.on('mouse:up', function(opt) {
        this.isDragging = false;
        this.selection = true;
        let objects = this.getObjects();
        for(let i = 0; i < objects.length; i++) {
          objects[i].setCoords();
        }
      });
    }
  }, [editorCanvas]);

  // OCR/Font Recognition
  useEffect(() => {
    if (!editorCanvas || recognisedTexts.length === 0) {
      return
    }

    const imgSrc = `${baseURL}/${ocrImageURL}`;
    fabric.Image.fromURL(imgSrc, image => {
      // Will assume the artboard object is always at the bottom of the stack
      const artBoard = editorCanvas.item(0);
      const layerCount = layers.length;
      let canvasObjects = {}

      // Adding image layer first
      if (image.height > artBoard.height) {
        image.scaleToHeight(artBoard.height);
      }
      const point = new fabric.Point(editorCanvas.width/2, editorCanvas.height/2);
      image.setPositionByOrigin(point, 'center', 'center');
      editorCanvas.add(image);
      const imageUuid = uuidv4();
      canvasObjects[imageUuid] = image;

      const imageLayer: Layer = {
        previewImg: imgSrc,
        title: `Layer ${layerCount+1}`,
        type: 'Image Layer',
        visibility: true,
        objectKeys: [imageUuid]
      }
      addLayer(imageLayer);

      // Now add the text layer
      let textLayer: Layer = {
        previewImg: '',
        title: `Layer ${layerCount+2}`,
        type: 'Text Layer',
        visibility: true,
        objectKeys: []
      }

      const newTextBoxes = recognisedTexts.map(payload => {
        const textbox = new fabric.Textbox(payload.text, {
          left: (payload.ratioLeft * artBoard.width) + artBoard.left,
          top: payload.ratioTop * artBoard.height,
          fontSize: payload.fontSize,
          fontFamily: payload.fontFamily,
        });
        editorCanvas.add(textbox);
        const textboxUuid = uuidv4();
        canvasObjects[textboxUuid] = textbox;
        textLayer.objectKeys.push(textboxUuid);
      });
      addLayer(textLayer);

      addCanvasObjects(canvasObjects);

      editorCanvas.renderAll();
    });

  }, [recognisedTexts]);

  // Color Separation
  useEffect(() => {
    if (!editorCanvas || colorOutputs.length === 0) {
      return
    }

    // Will assume the artboard object is always at the bottom of the stack
    const artBoard = editorCanvas.item(0);

    colorOutputs.forEach((output: ColorOutputObject, index: number) => {
      const imgSrc = `${baseURL}/${output.filepath}`;
      fabric.Image.fromURL(imgSrc, image => {
        if (image.height > artBoard.height) {
          image.scaleToHeight(artBoard.height);
        }
        const point = new fabric.Point(editorCanvas.width/2, editorCanvas.height/2);
        image.setPositionByOrigin(point, 'center', 'center');
        editorCanvas.add(image);
        const uuid = uuidv4();
        addCanvasObjects({ [uuid]: image });

        let newLayer: Layer = {
          previewImg: imgSrc,
          title: `${output.color_type} Layer ${output.index}`,
          type: 'Color Layer',
          visibility: true,
          objectKeys: [uuid]
        }
        addLayer(newLayer);
      });
    });
    editorCanvas.renderAll();

  }, [colorOutputs])

  const canvasStyle = {
    width: 'inherit',
    height: 'inherit',
  };

  return (
    <canvas
      ref={canvasElem}
      id={editorCanvasId}
      className={style.canvas}
      style={canvasStyle}
    />
  )
}

export default EditorCanvas;
