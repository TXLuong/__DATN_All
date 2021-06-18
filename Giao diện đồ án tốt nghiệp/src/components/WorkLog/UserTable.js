import React from 'react';
import {withStyles, makeStyles} from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead'
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

const StyledTableCell = withStyles((theme) => ({
	head : {
		backgroundColor : theme.palette.common.black,
		color : theme.palette.common.white,
	},
	body : {
		fontSize : 14,
	},
}))(TableCell);

const StyledTableRow = withStyles ((theme) => ({
	root: {
		'& : nth-of-type(odd)' : {
			backgroundColor : theme.palette.action.hover,
		},
	},
}))(TableRow);

function createData (day, timeIn, timeOut, totalTime){
	return {day, timeIn, timeOut, totalTime}
}
const rows = [
	createData("Alex", "8h10", "18h10", "8h", "4-5-2021"),
	createData("Alex", "8h10", "18h10", "8h", "4-5-2021"),
	createData("Alex", "8h10", "18h10", "8h", "4-5-2021"),
	createData("Alex", "8h10", "18h10", "8h", "4-5-2021")
];

const useStyles = makeStyles({
	table : {
		minWidth : 700,
	}
	,
});

export default function UserTable (props) {
	const classes = useStyles();
	return (
		 <TableContainer component={Paper}>
      <Table className={classes.table} aria-label="customized table">
        <TableHead>
          <TableRow>
            <StyledTableCell>Day</StyledTableCell>
            <StyledTableCell align="center">Time in</StyledTableCell>
            <StyledTableCell align="center">Time out</StyledTableCell>
            <StyledTableCell align="center">Total time &nbsp;(hour)</StyledTableCell>
            {/* <StyledTableCell align="right">Protein&nbsp;(g)</StyledTableCell> */}
          </TableRow>
        </TableHead>
        <TableBody>
          {props.rows.map((row) => (
            <StyledTableRow key={row.day}>
              <StyledTableCell component="th" scope="row">
                {row.day}
              </StyledTableCell>
              <StyledTableCell align="center">{row.timeIn}</StyledTableCell>
              <StyledTableCell align="center">{row.timeOut}</StyledTableCell>
              <StyledTableCell align="center">{row.totalTime}</StyledTableCell>
              {/* <StyledTableCell align="right">{row.protein}</StyledTableCell> */}
            </StyledTableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
	);
}

	
	

	

