import React from 'react'
var Route = require('react-router').Route
var Switch = require('react-router').Switch

import Home from "./../containers/Home.jsx";
import Users from "./../containers/Users.jsx";





const Routers = () => (
  <React.Fragment>
    <Switch>
      <Route exact path="/" component={Home} />

      <Route path="/users" component={Users} />
      {/* <Redirect from="/accounts" to="/users" /> */}

      {/* <Route component={NoMatch} /> */}
    </Switch>
  </React.Fragment>
)


export default Routers;

