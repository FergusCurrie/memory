import { Box, Button, Card, CardContent, Typography } from '@mui/material';
import React, { useState, useEffect, useRef } from 'react';

interface NextCardManagementProps {
  testPassed: boolean;
  handleScore: (result: boolean) => void;
}

const NextCardManagement: React.FC<NextCardManagementProps> = ({ testPassed, handleScore }) => {
  return (
    <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-between' }}>
      <Button
        variant="contained"
        color="error"
        onClick={() => handleScore(false)}
        sx={{ flex: 1, mr: testPassed ? 1 : 0 }}
      >
        Incorrect
      </Button>
      {testPassed && (
        <Button
          variant="contained"
          color="success"
          onClick={() => handleScore(true)}
          sx={{ flex: 1, ml: 1 }}
        >
          Correct
        </Button>
      )}
    </Box>
  );
};

export default NextCardManagement;
