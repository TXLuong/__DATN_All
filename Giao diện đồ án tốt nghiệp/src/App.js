import Admin from './layouts/Admin';
import SignIn  from './layouts/SignIn';
import {Route, Switch} from 'react-router-dom';
import globalRoutes from './globalRoutes';
import React from 'react';

function App() {
  const showContentMenus = (globalRoutes) => {
    var result = null;
    if(globalRoutes.length > 0){
      result = globalRoutes.map((route, index) => {
        return <Route key={index} path={route.path} component={route.main} exact={route.exact} />
      })
    }
    return result;
  }
  return (
      <div>
        <Switch>
          {showContentMenus(globalRoutes)}
        </Switch>
      </div>
    );
}

export default App;
