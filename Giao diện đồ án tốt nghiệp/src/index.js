/*!

=========================================================
* Material Dashboard React - v1.9.0
=========================================================

* Product Page: https://www.creative-tim.com/product/material-dashboard-react
* Copyright 2020 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/material-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React from "react";
import ReactDOM from "react-dom";
import { createBrowserHistory } from "history";
import { Router, Route, Switch, Redirect } from "react-router-dom";
import App from './App';
// core components
import Admin from "layouts/Admin.js";
import SignIn from "./layouts/SignIn";
import "assets/css/material-dashboard-react.css?v=1.9.0";
import AfterLogin from './layouts/AfterLogin'
import AppRouter from './AppRouter';
import {createLogger} from "redux-logger";
import thunkMiddleware from 'redux-thunk';
import {Provider} from 'react-redux';
import auth from './reducers/auth';
import {applyMiddleware, createStore} from "redux";
import { composeWithDevTools } from "redux-devtools-extension";
import Routes from "Routes";
import SignInContainer from './container/SignInContainer';
import appReducer from './reducers/index';
import {LOGOUT_SUCCESS} from '../src/action/Auth';
const blazeface = require("@tensorflow-models/blazeface");

console.log("blaze face is awesome", blazeface);

// *******  here is code to test blaze face
// async function test() {
//   const newImage = document.createElement('img');
//   newImage.setAttribute('src', "https://st.depositphotos.com/1008939/1880/i/600/depositphotos_18807295-stock-photo-portrait-of-handsome-man.jpg");
//   newImage.classList.add("no-mask-img");
//   // load the model 
//   print("newImage", newImage);
//   const model = await blazeface.load();
//   // passing in an image or video to the model. The model returnes an array of arrays
//   // of bounding boxes, probabilities, and landmarks, one for each detected face.
//   print("before error")
//   const returnTensors = false;
//   const predictions = await model.estimateFaces(newImage, returnTensors);
//   // const predictions = [1,2];
//   if (predictions.length > 0) {
//     // predictions is an array of objects describing each detected face.
//     for (let i = 0; i < predictions.length; i++) {
//       const start = predictions[i].left;
//       const end = predictions[i].right;
//       const size = [end[0] - start[0], end[1] - start[1]];
//       console.log("start: " + start , ", end: " + end , ", size: " + size);
//     }
//   }
//   else {
//     console.log("can not reach here");
//   }
// }
// test();

// // here is the ending 
const loggerMiddleware = createLogger();
let middleware = [
  thunkMiddleware,
];
middleware = [...middleware, loggerMiddleware];
var startState = {};
if (localStorage.getItem("TOKEN") !== null && localStorage.getItem("TOKEN") !== "null"){
  console.log("Not null token --------------------------------");
  startState = {
    auth : {
      token : localStorage.getItem("TOKEN"),
      isAuthenticated : true,
      roleid : localStorage.getItem("roleid"),
    },
  };
}
else {
  startState = {
    auth : {
      token : null,
      isAuthenticated : false,
      roleid : null,
    }
  }
}
const rootReducer = (state, action) => {
  if (action.type === "LOGOUT_SUCCESS"){
    state = undefined;
    console.log("undefined");
  }
  return appReducer(state, action);
}
console.log("before createStore ")
const store = createStore(rootReducer, startState, composeWithDevTools(applyMiddleware(...middleware)));
console.log("trang thai khoi tao")
console.log(startState)
store.subscribe(() => {
  console.log("log getState : " , store.getState());
  localStorage.setItem("TOKEN", store.getState().auth.token);
  localStorage.setItem("roleid", store.getState().auth.roleid);
});
const hist = createBrowserHistory();


// ReactDOM.render(
//   <Router history={hist}>
//     <Switch>
//       <Route path="/" component={SignIn} />
//       <Redirect from="/" to="/admin" />
//     </Switch>
//   </Router>,
//   document.getElementById("root")
// );


// ReactDOM.render(
//   <Router history={hist}>
//     <Switch>
//       <Route path="/admin" component={Admin} />
//       <Redirect from="/" to="/admin/dashboard" />
//     </Switch>
//   </Router>,
//   document.getElementById("root")
// );



// ReactDOM.render(
//   <Router history={hist}>
//     <AfterLogin></AfterLogin>
//   </Router>,
//   document.getElementById("root")
// );

ReactDOM.render(
 <Provider store={store}>
    <AppRouter/>,
 </Provider>,
  document.getElementById("root")
);


// ReactDOM.render(
//    <Provider store={store}>
//          <Routes></Routes>
//    </Provider>,
//     document.getElementById("root")
// );

// ReactDOM.render(
//   <Router history={hist}>
//     <Switch>
//       <Route path="/admin" component={Admin} />

//       <Redirect from="/" to="/admin/dashboard" />
//     </Switch>
//   </Router>,
//   document.getElementById("root")
// );