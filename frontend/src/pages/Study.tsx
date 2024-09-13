import React, { useState } from 'react';
import { Box, Select, MenuItem, SelectChangeEvent } from '@mui/material';
import StudyBasic from '../components/StudyBasic';
import StudyCode from '../components/StudyCode';

const Study: React.FC = () => {
  const [cardType, setCardType] = useState<'basic' | 'code'>('basic');

  const handleCardTypeChange = (event: SelectChangeEvent<'basic' | 'code'>) => {
    setCardType(event.target.value as 'basic' | 'code');
  };

  return (
    <Box sx={{ maxWidth: 1200, margin: 'auto', mt: 4 }}>
      <Select value={cardType} onChange={handleCardTypeChange} fullWidth sx={{ mb: 2 }}>
        <MenuItem value="basic">Basic</MenuItem>
        <MenuItem value="code">Code</MenuItem>
      </Select>
      {cardType === 'basic' ? <StudyBasic /> : <StudyCode />}
    </Box>
  );
};

export default Study;
