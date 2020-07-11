export interface ColorOutputObject {
  color_type: string;
  filepath: string;
  height: number;
  hue: number;
  hue_variance: number;
  index: number;
  width: number;
}

export interface ApiResponse {
  layers?: ColorOutputObject[];
}

export interface ColorSeparationState {
  colorOutputs: ColorOutputObject[];
}

// Action Types
export const SET_COLOR_OUTPUTS = 'SET_COLOR_OUTPUTS';
export type SET_COLOR_OUTPUTS = typeof SET_COLOR_OUTPUTS;
export interface SetColorOutputs {
  type: SET_COLOR_OUTPUTS;
  outputs: ColorOutputObject[];
}


export type ColorSeparationActions = SetColorOutputs;
