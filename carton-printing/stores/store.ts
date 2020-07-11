import { createStore, combineReducers, applyMiddleware } from 'redux'
import { composeWithDevTools } from 'redux-devtools-extension'
import { ocrInitialState, ocrReducer } from './ocr';
import { csInitialState, csReducer } from './color-separation';
import { editorInitialState, editorReducer } from './editor';

const appInitialState = {
}

const appReducer = (state = appInitialState, action) => {
  return state;
}

const combinedState = {
  appReducer: {
    ...appInitialState,
  },
  editorReducer: {
    ...editorInitialState,
  },
  ocrReducer: {
    ...ocrInitialState,
  },
  csReducer: {
    ...csInitialState,
  },
}

export const initializeStore = (preloadedState = combinedState) => {
  const reducers = combineReducers({ appReducer, editorReducer, ocrReducer, csReducer });
  return createStore(
    reducers,
    preloadedState,
    composeWithDevTools(applyMiddleware())
  )
}
