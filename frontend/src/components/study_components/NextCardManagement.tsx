import { Box, Button, Card, CardContent, Typography } from '@mui/material';
import React, { useState, useEffect, useRef } from 'react';

interface NextCardManagementProps {
  testPassed?: boolean;
  handleScore: (result: boolean) => void;
  answer?: string;
}

const NextCardManagement: React.FC<NextCardManagementProps> = ({
  testPassed,
  handleScore,
  answer,
}) => {
  const handleIncorrect = () => {
    alert(`The correct answer was: ${answer}`);
    handleScore(false);
  };

  return (
    <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-between' }}>
      <Button
        variant="contained"
        color="error"
        onClick={() => handleIncorrect(false)}
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
