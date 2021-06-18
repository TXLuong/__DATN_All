import React from 'react';
import Camera from 'react-html5-camera-photo';
import 'react-html5-camera-photo/build/css/index.css';

function CamHtml (props) {
  
  function handleTakePhoto (dataUri) {
    // Do stuff with the photo...
    // console.log(dataUri);
    props.handleChangeImage(dataUri);
    console.log('taked Photo');
  }
 
  return (
    <Camera 
      id = "cam"
      onTakePhoto = { (dataUri) => { handleTakePhoto(dataUri); } }
    />
  );
}
 
export default CamHtml;