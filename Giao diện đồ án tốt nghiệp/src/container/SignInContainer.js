import {connect} from 'react-redux';
import {login} from '../action/Auth';
import SignIn from '../layouts/SignIn';
const mapStateToProps = state1 => ({ // query de lay ra cac state 
    isAuthenticated: state1.auth.isAuthenticated,
    isRequest: state1.auth.isRequest,
    error: state1.auth.errorState,
    errorMsg: state1.auth.errorMsg,
    roleid : state1.auth.roleid
});// dinh nghia state.auth trong reducers.auth

const mapDispatchToProps = dispatch => ({
    requestLogin : (username, password) => dispatch(login(username, password)),
});

export default connect(mapStateToProps, mapDispatchToProps)(SignIn);

