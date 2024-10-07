import React, { useState, useEffect, useRef } from 'react';
import api from '../api';
import PolarsProblem from './problem_types/PolarsProblem';
import { Box, Typography } from '@mui/material';

interface Problem {
  problem_type: string;
  problem_id: number;
  //concept_id: number;
  code_default: string;
  datasets: string;
  description?: string;
  answer: string;
  //hint: string;
}

interface Remaining {
  remaining: number;
}

const Study: React.FC = () => {
  /**
   * Study Component
   *
   *
   * How does component memoyr work? do i need all state in this guy?
   *
   *
   * State:
   * - concept: An array of Concept objects fetched from the API
   *
   * Effects:
   * - Fetches concepts when the component mounts
   *
   * Functions:
   * - fetchConcepts: Asynchronous function to fetch concepts from the API
   *
   * @returns JSX.Element
   */

  const [problem, setProblem] = useState<Problem>();
  const [problemsRemaining, setProblemsRemaining] = useState<boolean>(true);
  const [numberProblemsRemaining, setNumberProblemsRemaining] = useState<number>(0);

  useEffect(() => {
    fetchProblemsRemaining();
    fetchConcept();
  }, []);

  const fetchProblemsRemaining = async () => {
    const response = await api.get('/api/problem/get_number_problems_remaining');
    setNumberProblemsRemaining(response.data.remaining);
  };

  const handleScore = async (result: boolean) => {
    /**
     * Handles the scoring of a problem.
     *
     * This function is called when the user submits their answer to a problem.
     * It sends a POST request to the API to record the result, then fetches a new problem.
     *
     * @param {boolean} result - Whether the user's answer was correct (true) or incorrect (false)
     * @returns {Promise<void>}
     */
    if (problem) {
      try {
        console.log('Handling score');
        await api.post('/api/review', {
          problem_id: problem.problem_id,
          result: result,
        });
        fetchProblemsRemaining();
        fetchConcept();
      } catch (error) {
        console.error('Error submitting review:', error);
      }
    }
  };

  const fetchConcept = async () => {
    try {
      console.log('requesting');
      const response = await api.get('/api/problem/get_next_problem');
      if (response.data.problems.length === 0) {
        setProblemsRemaining(false);
      } else {
        console.log(response.data.problems[0])
        setProblem(response.data.problems[0]);
      }
    } catch (error) {
      console.error('Error fetching concept', error);
    }
  };

  return (
    <>
      <Typography>Remaining probs = {numberProblemsRemaining}</Typography>
      {problemsRemaining ? (
        <Box sx={{ maxWidth: 1200, margin: 'auto', mt: 4 }}>
          {problem?.problem_type === 'polars' && (
            <PolarsProblem problem={problem} handleScore={handleScore} />
          )}
        </Box>
      ) : (
        <Typography variant="h5" sx={{ textAlign: 'center', mt: 4 }}>
          No cards remaining
        </Typography>
      )}
    </>
  );
};

export default Study;
