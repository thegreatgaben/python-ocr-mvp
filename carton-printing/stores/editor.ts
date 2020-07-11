import {
  EditorState,
  EditorActions,
  SET_CANVAS,
  ADD_CANVAS_OBJECTS,
  ADD_LAYER,
  UPDATE_LAYER,
  TOGGLE_LAYER_VISIBILITY
} from '../typings/editor.d'

export const editorInitialState: EditorState = {
  editorCanvas: undefined,
  canvasObjects: {},
  layers: [
    {
      previewImg: '/static/editor/init.png',
      title: 'Layer 1',
      type: 'Artboard',
      visibility: true,
      objectKeys: [],
    }
  ],
}

export const editorReducer = (
  state: EditorState = editorInitialState,
  action: EditorActions
): EditorState => {
  switch (action.type) {
    case SET_CANVAS:
      return {
        ...state,
        editorCanvas: action.canvas,
      };
    case ADD_CANVAS_OBJECTS:
      return {
        ...state,
        canvasObjects: {
          ...state.canvasObjects,
          ...action.objects,
        }
      }
    case ADD_LAYER:
      return {
        ...state,
        layers: [...state.layers, action.layer],
      };
    case UPDATE_LAYER: {
      const updatedLayers = [...state.layers];
      updatedLayers[action.layerIndex][action.key] = action.value;
      return {
        ...state,
        layers: updatedLayers,
      };
    }
    case TOGGLE_LAYER_VISIBILITY: {
      // Hide all objects that are in the selected layer
      const layer = state.layers[action.layerIndex];
      layer.objectKeys.forEach(key => {
        const canvasObj = state.canvasObjects[key];
        canvasObj.visible = action.visibility;
      });
      state.editorCanvas.renderAll();

      const updatedLayers = [...state.layers];
      updatedLayers[action.layerIndex].visibility = action.visibility;
      return {
        ...state,
        layers: updatedLayers,
      }
    }
    default:
      return state;
  }
}
