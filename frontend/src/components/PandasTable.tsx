import React from 'react';
import {
  Table,
  TableHead,
  TableCell,
  TableRow,
  TableContainer,
  TableBody,
  Paper,
} from '@mui/material';

const PandasJsonTable = ({ data }) => {
  // Check if data is empty or undefined
  if (!data || Object.keys(data).length === 0) {
    return <></>; // Return empty fragment if data is empty
  }
  // Extract column names from the first row
  const columns = Object.keys(data);

  // Get the number of rows (assuming all columns have the same length)
  const rowCount = Object.keys(data[columns[0]]).length;

  // Function to format cell values
  const formatCellValue = (value) => {
    if (typeof value === 'number') {
      return value.toFixed(4); // Format numbers to 4 decimal places
    }
    return value;
  };

  return (
    <TableContainer component={Paper} sx={{ maxHeight: 400 }}>
      <Table size="small" stickyHeader aria-label="pandas dataframe table">
        <TableHead>
          <TableRow>
            {columns.map((column) => (
              <TableCell
                key={column}
                sx={{ py: 1, px: 2, fontWeight: 'bold', bgcolor: 'lightblue' }}
              >
                {column}
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {[...Array(rowCount)].map((_, rowIndex) => (
            <TableRow key={rowIndex}>
              {columns.map((column) => (
                <TableCell key={`${column}-${rowIndex}`} sx={{ py: 0.5, px: 2 }}>
                  {formatCellValue(data[column][rowIndex.toString()])}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default PandasJsonTable;
