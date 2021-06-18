import { useState } from 'react';
import React from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  Divider,
  Grid,
  TextField
} from '@material-ui/core';
import { instanceOf } from 'prop-types';


const AccountProfileDetails = (props) => {

  const [values, setValues] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
  });
  const handleFirstNameChange = (e) => {
    setValues({...values, firstName : e.target.value});
    let temp = {...values, firstName : e.target.value};
    props.handleChildChanges(temp);

  }
  const handleLastNameChange = (e) => {
    setValues({...values, lastName : e.target.value});
    let temp = {...values, lastName : e.target.value};
    props.handleChildChanges(temp);
  }
  const handleEmailChange = (e) => {
    setValues({...values, email : e.target.value});
    let temp = {...values, email : e.target.value};
    props.handleChildChanges(temp);
  }
  const handlePhoneChange = (e) => {
    setValues({...values, phone : e.target.value});
    let temp = {...values, phone : e.target.value};
    props.handleChildChanges(temp);
  }
  return (
    <form
      autoComplete="off"
      noValidate
      {...props}
    >
      <Card>
        <CardHeader
          subheader="Add new employee"
          title="Employee information"
        />
        <Divider />
        <CardContent>
          <Grid
            container
            spacing={3}
          >
            <Grid
              item
              md={6}
              xs={12}
            >
              <TextField
                fullWidth
                // helperText="Please specify the first name"
                label="First name"
                name="firstName"
                onChange={handleFirstNameChange}
                required
                value={values.firstName}
                variant="outlined"
              />
            </Grid>
            <Grid
              item
              md={6}
              xs={12}
            >
              <TextField
                fullWidth
                label="Last name"
                name="lastName"
                onChange={handleLastNameChange}
                required
                value={values.lastName}
                variant="outlined"
              />
            </Grid>
            <Grid
              item
              md={6}
              xs={12}
            >
              <TextField
                fullWidth
                label="Email Address"
                helperText="Please specify the email"
                name="email"
                onChange={handleEmailChange}
                required
                value={values.email}
                variant="outlined"
              />
            </Grid>
            <Grid
              item
              md={6}
              xs={12}
            >
              <TextField
                fullWidth
                label="Phone Number"
                name="phone"
                onChange={handlePhoneChange}
                required
                value={values.phone}
                variant="outlined"
              />
            </Grid>
            {/* <Grid
              item
              md={6}
              xs={12}
            >
              <TextField
                fullWidth
                label="Country"
                name="country"
                onChange={handleChange}
                required
                value={values.country}
                variant="outlined"
              />
            </Grid> */}
            {/* <Grid
              item
              md={6}
              xs={12}
            >
              <TextField
                fullWidth
                label="Select State"
                name="state"
                onChange={handleChange}
                required
                select
                SelectProps={{ native: true }}
                value={values.state}
                variant="outlined"
              >
                {states.map((option) => (
                  <option
                    key={option.value}
                    value={option.value}
                  >
                    {option.label}
                  </option>
                ))}
              </TextField>
            </Grid> */}
          </Grid>
        </CardContent>
        <Divider />
        {/* <Box
          sx={{
            display: 'flex',
            justifyContent: 'flex-end',
            p: 2
          }}
        >
        <div text-align="center">
          <Button
            color="primary"
            variant="contained"
            margin = '200'
          >
            Save details
          </Button>
        </div>
        </Box> */}
      </Card>
    </form>
  );
};

export default AccountProfileDetails;
