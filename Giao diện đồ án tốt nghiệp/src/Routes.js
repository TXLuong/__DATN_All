import React, {Suspense} from 'react';
import {Route, Switch} from 'react-router-dom';
import SignInContainer from './container/SignInContainer';
import dashboardRoutes from 'routes';
export default function Routes(props) {
    return (
        <Suspense>
            <Switch>
                <Route component={SignInContainer} path = "/login"></Route>
                <Route component={dashboardRoutes} path = "*"></Route>
            </Switch>
        </Suspense>
    )
}