import React from 'react'
import SignIn from './layouts/SignIn'
import AfterLogin from './layouts/AfterLogin'

const globalRoutes = [
    { path: '/',
      exact: true,
      main : () => <SignIn/>
    },
    { path: '/admin',
      exact: true,
      main: () => <AfterLogin/>,
    },
    
]

export default globalRoutes;