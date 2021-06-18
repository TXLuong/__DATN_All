import React from 'react';
import {Switch, Route, Redirect} from 'react-router-dom';
import Admin from './Admin'

export default function AfterLogin() {
    return (
        <Switch>
            <Route path="/admin" component={Admin} />
            <Redirect from="/" to="/admin/dashboard" />
        </Switch>
    )
}