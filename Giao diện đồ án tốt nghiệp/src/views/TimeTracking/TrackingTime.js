import React, {useState, useEffect,useCallback, useRef} from 'react';
import Button from '../../components/CustomButtons/Button';
import { makeStyles } from '@material-ui/core/styles';
import { useHistory } from "react-router-dom";
import Webcam from 'react-webcam';

const blazeface = require("@tensorflow-models/blazeface");

export default function TrackingTime() {
    return (
        <div>
            <Webcam></Webcam>
            <Button>Take a photo</Button>
        </div>
    )
}