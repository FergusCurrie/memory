import React, { useState, useEffect } from 'react';
import { Typography, Radio, RadioGroup, FormControlLabel, Button, Paper, Box } from '@mui/material';
import Description from '../study_components/Description';
import NextCardManagement from '../study_components/NextCardManagement';
import api from '../../api';

interface Problem {
  problem_type: string;
  problem_id: number;
}

interface cardProblemData {
  front: string;
  back: string;
}

interface CardProblemInterface {
  problem: Problem;
  handleScore: (result: boolean) => void;
}

const CardProblem: React.FC<CardProblemInterface> = ({ problem, handleScore }) => {
  const [cardProblemData, setCardProblemData] = useState<cardProblemData>();
  const [showBack, setShowBack] = useState<boolean>(false);

  // ... existing useEffect and other functions ...

  const handleShowBack = () => {
    setShowBack(true);
  };

  const fetchcardProblemData = async () => {
    try {
      const response = await api.get(`/api/problem/card/${problem.problem_id}`);
      console.log(response);
      setCardProblemData(response.data);
    } catch (error) {
      console.error('Error fetching card problem data', error);
    }
  };

  useEffect(() => {
    if (problem) {
      fetchcardProblemData();
    }
  }, [problem]);

  return (
    <>
      <Description text={cardProblemData?.front} />
      {!showBack ? (
        <Box mt={2}>
          <Button variant="contained" color="primary" onClick={handleShowBack}>
            Show Back
          </Button>
        </Box>
      ) : (
        <Description text={cardProblemData?.back} />
      )}
      <NextCardManagement {...{ testPassed: true, handleScore, answer: cardProblemData?.back }} />
    </>
  );
};

export default CardProblem;
