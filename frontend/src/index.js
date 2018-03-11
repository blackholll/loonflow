import React from 'react'
import ReactDOM from 'react-dom';
import { Router } from 'react-router'
import createBrowserHistory from 'history/createBrowserHistory'
import 'antd/dist/antd.less';


const history = createBrowserHistory()

import BasicLayout from "./containers/BasicLayout/BasicLayout";

const App = () => (
  <Router history={history}>
    <div>
      <BasicLayout />
    </div>
  </Router>
)
ReactDOM.render(
  <App />,
  document.getElementById('root')
);
