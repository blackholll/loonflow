import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import App from './App';
import DynamicLocalizationProvider from './components/commonComponents/DynamicLocalizationProvider';
import './i18n/index';
import './index.css';
import reportWebVitals from './reportWebVitals';
import { persistor, store } from './store';


const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <DynamicLocalizationProvider>
          <App />
        </DynamicLocalizationProvider>
      </PersistGate>

    </Provider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
