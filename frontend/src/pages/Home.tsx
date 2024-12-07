import React, { useState, useEffect } from 'react';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { Box } from '@mui/material';
import api from '../api';

// Functional Component using React Hooks
const Home = () => {
  // const handleSyncDb = async () => {
  //   try {
  //     const response = await api.post('/api/sync_db');
  //     console.log(response.data.message);
  //     // You might want to show a success message to the user here
  //   } catch (error) {
  //     console.error('Error syncing database:', error);
  //     // You might want to show an error message to the user here
  //   }
  // };
  return (
    <div>
      {/* ... (existing JSX) */}
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh" // This ensures the box takes up the full height of the viewport
      >
        <Typography>Spaced memory</Typography>
      </Box>
      {/* ... (rest of the existing JSX) */}
    </div>
  );
};

export default Home;
