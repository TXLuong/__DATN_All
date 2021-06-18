import React from 'react';
import AccountProfileDetails from '../../components/Account/EmployeeAccount';
import UpLoadImg from '../../components/Account/UpLoadImg';
import Button from '../../components/CustomButtons/Button';
import {useState} from 'react';
import {useSelector, useDispatch} from 'react-redux';
import { authPost } from '../../api';

import { makeStyles } from '@material-ui/core/styles';
import Alert from '@material-ui/lab/Alert';
import IconButton from '@material-ui/core/IconButton';
import Collapse from '@material-ui/core/Collapse';
import CloseIcon from '@material-ui/icons/Close';

const useStyles = makeStyles((theme) => ({
    root: {
      width: '100%',
      '& > * + *': {
        marginTop: theme.spacing(2),
      },
    },
  }));

export default function AddEmployee(){
    const token =  useSelector((state) => state.auth.token);
    const dispatch = useDispatch();
    const [open, setOpen] = useState(false);
    const [values, setValues] = useState({
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
    });
    const [imageUrl, setImageUrl] = useState(null);
    const handleChildImage = (base64) => {
        
        setImageUrl(base64);
    }
    const handleChildChanges = (val) => {
        setValues(val);
    }

    const onClick = () => {
        let data = {
            "infor" : values,
            'face' : imageUrl
        }
        authPost(dispatch, token, "/addEmployee", data).then(
            (res) =>{
                if(res.status){
                    setOpen(true);
                }
            }
        );
        // location.reload();
        setValues(null);
        setImageUrl(null);
    }
    return (
        <>
        <Collapse in={open}>
            <Alert
            action={
                <IconButton
                aria-label="close"
                color="inherit"
                size="small"
                onClick={() => {
                    setOpen(false);
                    location.reload();
                }}
                >
                <CloseIcon fontSize="inherit" />
                </IconButton>
            }
            >
            Create new employee success!
            </Alert>
         </Collapse>
            <AccountProfileDetails handleChildChanges={handleChildChanges}/>
            <div style = {{color: "green", textAlign: "center", margin : '20px'}}>
            <UpLoadImg handleChildImage = {handleChildImage} ></UpLoadImg>
            </div>
            <div style = {{color:  "red", textAlign: "center", margin : '20px'}}>
                <Button onClick = {onClick}> Add new employee </Button>
            </div>
        </>
    )
}