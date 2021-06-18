import React from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import { Redirect, useLocation, useHistory } from "react-router-dom";
import {useState, useEffect} from 'react';
import backGroundImage from '../../src/assets/img/workBackGround.jpg';
function Copyright() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {'Copyright © '}
      <Link color="inherit" href="https://material-ui.com/">
        Your Website
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const useStyleForBackground = makeStyles((theme) => ({
  container: {
    color  : 'red',
    backgroundColor : "green", 
  },
  image : {
    position: "absolute",
    width: "100vw",
    height: "100vh",
    top : 0,
    bottom : 0, 
  },
  link : {
    color : "green",
  }
}))

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

export default function SignIn(props) {
  const classesForBackground = useStyleForBackground();
  const [email, setEmail] = useState(""); // email 
  const [password, setPassword] = useState(""); // password 
  const classes = useStyles();
  const [statusLogin, setStatusLogin] = React.useState(false);
  const history = useHistory();
  const handleLogIn = (e) => {
    console.log("adcad");
    e.preventDefault();
    console.log(`username ${email}` + `password ${password}`);
    props.requestLogin(email, password);
  }
  const handleEmail = (e) => {
    setEmail(e.target.value);
    console.log(email);
  }
  const handlePassword = (e) =>{
    setPassword(e.target.value);
  }
  if(props.isAuthenticated === true) {
    console.log("----------------------------------------------------------------", props.roleid);
    if(props.roleid == '1'){
      return (
        <Redirect to='/admin' />
      )
    }
    else if (props.roleid == '2') {
      console.log("employee is ready");
      return (
        <Redirect to='/employee'/>
      );
    }
  }
  else return (
  <div>
    <img alt = "welcome" src = {backGroundImage} className = {classesForBackground.image}></img>
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <Avatar className={classes.avatar}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Sign in
        </Typography>
        <form className={classes.form} noValidate>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="email"
            label="Email Address"
            name="email"
            autoComplete="email"
            autoFocus
            onChange = {handleEmail}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
            onChange = {handlePassword}
          />
          <FormControlLabel
            control={<Checkbox value="remember" color="primary" />}
            label="Remember me"
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
            onClick = {handleLogIn}
          >
            Sign In
          </Button>
          <Grid container>
            <Grid item xs>
              <Link href="#" variant="body2" className={classesForBackground.link}>
                Forgot password?
              </Link>
            </Grid>
            <Grid item>
              <Link href="#" variant="body2">
                {"Don't have an account? Sign Up"}
              </Link>
            </Grid>
          </Grid>
        </form>
      </div>
      <Box mt={8}>
        <Copyright />
      </Box>
    </Container>
  </div>
  );
}