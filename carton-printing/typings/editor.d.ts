export interface Layer {
  previewImg: string,
  title: string,
  type: string,
  visibility: boolean,
  objectKeys: string[],
}

type FabricCanvas = any;
type FabricObjects = object;

export interface EditorState {
  editorCanvas: FabricCanvas;
  canvasObjects: FabricObjects;
  layers: Layer[];
}

// Action Types
export const SET_CANVAS = 'SET_CANVAS';
export type SET_CANVAS = typeof SET_CANVAS;
export interface SetCanvas {
  type: SET_CANVAS;
  canvas: FabricCanvas;
}

export const ADD_CANVAS_OBJECTS = 'ADD_CANVAS_OBJECTS';
export type ADD_CANVAS_OBJECTS = typeof ADD_CANVAS_OBJECTS;
export interface AddCanvasObjects {
  type: ADD_CANVAS_OBJECTS;
  objects: FabricObjects;
}

export const ADD_LAYER = 'ADD_LAYER';
export type ADD_LAYER = typeof ADD_LAYER;
export interface AddLayer {
  type: ADD_LAYER;
  layer: Layer;
}

export const UPDATE_LAYER = 'UPDATE_LAYER';
export type UPDATE_LAYER = typeof UPDATE_LAYER;
export interface UpdateLayer {
  type: UPDATE_LAYER;
  layerIndex: number;
  key: string;
  value: any;
}

export const TOGGLE_LAYER_VISIBILITY = 'TOGGLE_LAYER_VISIBILITY';
export type TOGGLE_LAYER_VISIBILITY = typeof TOGGLE_LAYER_VISIBILITY;
export interface ToggleLayerVisibility {
  type: TOGGLE_LAYER_VISIBILITY;
  layerIndex: number;
  visibility: boolean;
}

export type EditorActions = AddLayer | UpdateLayer | SetCanvas | ToggleLayerVisibility | AddCanvasObjects;
