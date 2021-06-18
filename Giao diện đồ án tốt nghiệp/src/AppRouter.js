import React from 'react';
import {BrowserRouter as Router, Link, Redirect, Route, Switch } from 'react-router-dom';
import Admin from './layouts/Admin';
import SignIn from './layouts/SignIn';
import SignInContainer from './container/SignInContainer';
import Employee from './layouts/Employee';
export default function AppRouter() {
    return (
        <Router>
            <Switch>
                <Route path = '/admin'>
                    <Admin/>
                </Route>
                <Route path = '/employee'>
                    <Employee/>
                </Route>
                <Route path = '/login'>
                    <SignInContainer/>
                </Route>
                <Route path = ''>
                    <Redirect to = "/login"></Redirect>
                </Route>
            </Switch>
        </Router>
    )
}                                                                   