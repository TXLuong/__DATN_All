import {API_URL} from '../config/config';
import base64 from "base-64";
import { IconContext } from "react-icons/lib/cjs";
import { Box } from "@material-ui/core";
import { toast } from "react-toastify";
import React from 'react';
import { MdCancel, MdWarning } from "react-icons/md";


export const LOGIN_REQUESTING = "LOGIN_REQUESTING";
export const LOGIN_SUCCESS = "LOGIN_SUCCESS";
export const LOGOUT_SUCCESS = "LOGOUT_SUCCESS";
export const LOGIN_FAILURE = "LOGIN_FAILURE";
export const ERROR = "ERROR";

export const logout = () => {
    return (dispatch, getState) => {
      dispatch(requesting()); // create a action
      const headers = new Headers();
  
  
      headers.append("Content-Type", "application/json");
      headers.append("X-Auth-Token", getState().auth.token);
  
      fetch(`${API_URL}/logout`, {
        method: "GET",
        headers: headers
      })
        .then(res => {
          if (res.ok) {
            dispatch(logoutsuccess());
          }
          return res.json();
        })
        .then(
          res => {
            // if (res.status === "SUCCESS") {
            //     dispatch(success());
            // } else{
            //     dispatch(failed());
            // }
          },
          error => {
            dispatch(failed());
          }
        );
    };
  
  }
  

export const login = (username, password) =>{
    const body = {
        username : username,
        password : password
    }
    console.log("body : ", body);
    console.log("Username: " + username + ", Password: " + password)
    return dispatch => {
        dispatch(requesting()); // create a action 
        const headers = new Headers();
        headers.set(
            "Authorization",
            base64.encode(username + ":" + password)
        );
        headers.append("Content-Type", "application/json");
        fetch(`${API_URL}/login`,{
            method: "POST",
            headers: headers,
            body: body,
        })
        .then(response =>{
            // save token from Server
            console.log("response ------------------------  ", response.text.toString);
            console.log("body ------------------------", response.body.getReader);
            console.log("body ------------------------", JSON.stringify(response.headers))
            console.log("headers ------------------------", response.headers);
            console.log("tojson ------------------------", response.json.toString)
            if (response.status === 401){
                dispatch(failed(true, "Username or password is incorrect"));
                errorNoti("Tài khoản hoặc mật khẩu không đúng");
            }
            return response.json();
        })
        .then(
            data =>
                {   console.log("delicious onion ");
                    console.log(data);
                    dispatch(success(data));
                }
        )
        .then(response =>{
        },
        error =>{

        });
    }
}

const requesting = () => {
    return {
        type : LOGIN_REQUESTING
    }
}

const success = data => {// token la tham so cua success 
    return {
        type : LOGIN_SUCCESS,
        token : data.token,
        roleid : data.roleid
    }
}

const sucessRoleid = roleid => {
    return {
        type : ROLE_SUCCESS,
        roleid : roleid
    }
}


const logoutsuccess = token => {
    return {
        type : LOGOUT_SUCCESS
    };
}

export const failed = (errorState = false, errorMsg = null) => {
    return {
        type : LOGIN_FAILURE,
        errorState : errorState,
        errorMsg : errorMsg
    }
}

const errorNoti = (message, autoClose) => {
  toast.error(
    <Box display="flex" alignItems="center">
      <IconContext.Provider>
        <MdCancel size={20} style={{ marginRight: "5px" }} />
      </IconContext.Provider>
      {message}
    </Box>,
    {
      position: "bottom-right",
      autoClose: autoClose === undefined ? false : autoClose,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
    }
)};

