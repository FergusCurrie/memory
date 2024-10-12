import React, { useState, useEffect } from 'react';
import { Typography, Radio, RadioGroup, FormControlLabel, Button, Paper, Box } from '@mui/material';
import Description from '../study_components/Description';
import api from '../../api';

interface Problem {
  problem_type: string;
  problem_id: number;
}

interface MultiChoiceProblemData {
  description?: string;
  options: string[];
  correctAnswer: string;
}

interface MCProblem {
  problem: Problem;
  handleScore: (result: boolean) => void;
}

const MultiChoiceProblem: React.FC<MCProblem> = ({ problem, handleScore }) => {
  const [testPassed, setTestPassed] = useState<boolean>();
  const [multiChoiceProblemData, setMultiChoiceProblemData] = useState<MultiChoiceProblemData>();
  const [selectedAnswer, setSelectedAnswer] = useState<string>('');

  const fetchMultiChoiceProblemData = async () => {
    try {
      const response = await api.get(`/api/problem/multi_choice/${problem.problem_id}`);
      console.log(response)
      setMultiChoiceProblemData(response.data);
    } catch (error) {
      console.error('Error fetching multi-choice problem data', error);
    }
  };

  useEffect(() => {
    if (problem) {
      fetchMultiChoiceProblemData();
      setTestPassed(false);
      setSelectedAnswer('');
    }
  }, [problem]);

  const handleAnswerSelection = (option: string) => {
    setSelectedAnswer(option);
  };

  const handleSubmit = () => {
    if (multiChoiceProblemData) {
      const isCorrect = selectedAnswer === multiChoiceProblemData.correctAnswer;
      console.log('Selected Answer:', selectedAnswer);
      console.log('Correct Answer:', multiChoiceProblemData.correctAnswer);
      console.log('Is Correct:', isCorrect);
      alert(isCorrect)
      setTestPassed(isCorrect);
      handleScore(isCorrect);
    }
  };

  return (
    <>
    <Description text={multiChoiceProblemData?.description} />
    <Paper elevation={3} sx={{ p: 3, maxWidth: 600, mx: 'auto' }}>
      
      {multiChoiceProblemData?.options && (
        <Box mt={2}>
          <RadioGroup
            value={selectedAnswer}
            onChange={(e) => handleAnswerSelection(e.target.value)}
          >
            {multiChoiceProblemData.options.map((option, index) => (
              <FormControlLabel
                key={index}
                value={option}
                control={<Radio />}
                label={option}
              />
            ))}
          </RadioGroup>
          <Box mt={2}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleSubmit}
              disabled={!selectedAnswer}
            >
              Submit Answer
            </Button>
          </Box>
        </Box>
      )}
      {testPassed !== null && (
        <Typography
          mt={2}
          color={testPassed ? 'success.main' : 'error.main'}
        >
          {testPassed ? "Correct!" : "Incorrect. Try again."}
        </Typography>
      )}
    </Paper>
    </>
  );
};

export default MultiChoiceProblem;
