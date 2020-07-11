import {ColorSeparationState, ColorSeparationActions, SET_COLOR_OUTPUTS} from '../typings/color-separation.d';

export const csInitialState: ColorSeparationState = {
  colorOutputs: []
}

export const csReducer = (
  state: ColorSeparationState = csInitialState,
  action: ColorSeparationActions
): ColorSeparationState => {
  switch (action.type) {
    case SET_COLOR_OUTPUTS:
      return {
        ...state,
        colorOutputs: action.outputs
      };
    default:
      return state;
  }
}
