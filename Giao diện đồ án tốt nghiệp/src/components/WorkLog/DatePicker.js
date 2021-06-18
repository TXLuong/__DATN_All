import React, {useRef, useState} from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';

const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 200,
  },
});

function DatePickers(props) {
  const { classes } = props;
  const [date, setDate] = useState("2021-05-29");
  const handleChange = (e) => {
    setDate(e.target.value);
    props.changeDate(e.target.value);
  }
  return (
    <form className={classes.container} noValidate >
      <TextField
        value={date}
        id="date"
        label={props.label}
        type="date"
        defaultValue="2021-05-24"
        className={classes.textField}
        InputLabelProps={{
          shrink: true,
        }}
        onChange = {handleChange}
      />
    </form>
  );
}

DatePickers.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(DatePickers);
