import React from 'react';
import {useState} from 'react';
export default function UpLoadImg(props) {
    const [imgUrl, setImgUrl] = useState(null);
    const convertBase64 = (file) => {
        return new Promise((resolve, reject) => {
          const fileReader = new FileReader();
          fileReader.readAsDataURL(file)
          fileReader.onload = () => {
            resolve(fileReader.result);
          }
          fileReader.onerror = (error) => {
            reject(error);
          }
        })
    }
    const onFileChange = async (event) => {
        const file = event.target.files[0];
        const base64 = await convertBase64(file);
        setImgUrl(base64);
        props.handleChildImage(base64);
    };
    
    return (
        <input type="file" onChange={onFileChange} />
    )
}