import React, { useCallback } from 'react';
import Button from '../../components/CustomButtons/Button';
import { makeStyles } from '@material-ui/core/styles';
import {useState, useEffect, useRef} from 'react';
import { useHistory } from "react-router-dom";
import Webcam from 'react-webcam';
import {authPost} from '../../api';
import {useSelector, useDispatch} from 'react-redux';
const blazeface = require("@tensorflow-models/blazeface");


const videoConstraints = {
  width: 1280,
  height: 720,
  facingMode : "user"
};



const styles = {
    root: {
        justifyContent: 'center'
    }
};
const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  button:{
    marginTop : '50px',
    padding : '10px',
    borderRadius : '10px',
    margin : '20px',
  },
  container: {
    textAlign: 'center',
  }
  }));  
const useStyleForButton = makeStyles((theme) => ({
  container: {
    display: 'block',
    textAlign : 'center',
  },
}))
  
export default function TrackingTime(){
    const classesContainButton = useStyleForButton();
    const classes = useStyles();
    const history = useHistory();
    const [uriImagetest, setUriImagetest] = useState("");
    const webcamRef = useRef(null);
    const [turnIn, setTurnIn] = useState(false);
    const token = useSelector(state => state.auth.token);
    const dispatch = useDispatch();
    const capture = useCallback(
      async () => {
        const imageSrc = webcamRef.current.getScreenshot();
        document.getElementById("imageFace").src = await imageSrc;
        // console.log(document.getElementById("hanhha"));
        // console.log(imageSrc);
        const model = await blazeface.load();
        const returnTensors = false;
        const predictions = await model.estimateFaces(document.getElementById("imageFace"), returnTensors);
        if(predictions.length > 0) {
        const start = predictions[0].topLeft;
        const end = predictions[0].bottomRight;
        const size = [end[0]-start[0], end[1]-start[1]];
        const idealWidth = size[0]+5;
        const idealHeight = size[1]+30;
        let tempCanvas = document.createElement("canvas");
        tempCanvas.width = 112;
        tempCanvas.height = 112;
        const ctx = tempCanvas.getContext("2d");
        ctx.drawImage(document.getElementById("imageFace"),start[0]-5,start[1]-30, idealWidth, idealHeight, 0, 0, 112, 112);
        console.log("finished ", tempCanvas.toDataURL());
        console.log(predictions[0]);
        setUriImagetest(tempCanvas.toDataURL());
        authPost(dispatch, token, "/turnIn", tempCanvas.toDataURL());
      }
      else {
        console.log("can not capture face ");
      }
      },
      [webcamRef]
    );
    useEffect(() => {
      if(window.opener)
      setInterval(() => {
        console.log("here we go");
        console.log(window.opener);
        console.log(window.top !== window.self);
        document.getElementById("captureButton").click();
      },1000*10)
    }, [])
    const openPopupWindow = () => {
      let windowObjectReference = window.open(
         history.location.pathname,
        "DescriptiveWindowName",
        "resizable,scrollbars,status,width = 400, height = 200"
      );
    }
    const handleClick = async () => {
      setTurnIn(true);
      openPopupWindow();
    }
    
    return (
        <div className={classes.container}>
            <Webcam ref = {webcamRef}>
            </Webcam>
            <img id = "imageFace" >
            </img>
            <div>
            <img src = {uriImagetest}></img>
            </div>
            <div className = {classesContainButton.container}>
            <Button id = "captureButton" className={classes.button} onClick = {capture}>Take a picture</Button>
            <Button className={classes.button} onClick={handleClick}>Turn in</Button>
            </div>
        </div>
    )
}