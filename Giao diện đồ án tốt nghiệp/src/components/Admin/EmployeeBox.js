/* eslint-disable no-use-before-define */
import React from 'react';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';

export default function EmployeeBox(props) {
  return (
    <Autocomplete
      id="combo-box-demo"
      options={props.employees}
      getOptionLabel={(option) => {
        props.setEmp_id(option.id);
        return option.fullname
      }}
      style={{ width: 170 }}
      renderInput={(params) => <TextField {...params} label="Employee box" variant="outlined" />}
    />
  );
}