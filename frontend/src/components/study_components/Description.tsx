import { Card, CardContent, Typography } from '@mui/material';
import React, { useState, useEffect, useRef } from 'react';

const Description: React.FC<{ text?: string }> = ({ text }) => {
  return (
    <Card>
      <CardContent>
        <Typography variant="h5" component="div" gutterBottom>
          Description:
        </Typography>
        <Typography variant="body1" paragraph>
          {text}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default Description;
