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
  console.log('Received data:', data); // Debugging: Log the received data

  // Parse the data if it's a string
  if (typeof data === 'string') {
    try {
      data = JSON.parse(data);
    } catch (error) {
      console.error('Error parsing JSON:', error);
      return <div>Error parsing data</div>;
    }
  }

  // Check if data is empty or undefined
  if (!data || Object.keys(data).length === 0) {
    return <div>No data available</div>;
  }

  // Extract column names
  const columns = Object.keys(data);

  // Get the number of rows
  const rowCount = Object.keys(data[columns[0]]).length;

  console.log('Columns:', columns); // Debugging: Log the columns
  console.log('Row count:', rowCount); // Debugging: Log the row count

  // Function to format cell values
  const formatCellValue = (value) => {
    if (value === null) return 'N/A';
    if (typeof value === 'number') {
      return value.toFixed(2); // Format numbers to 2 decimal places
    }
    return value;
  };

  if (rowCount === 0) {
    return <div>No rows found in the data</div>;
  }

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
          {Array.from({ length: rowCount }).map((_, rowIndex) => (
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
