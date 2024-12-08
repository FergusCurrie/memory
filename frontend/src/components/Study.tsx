import React, { useState, useEffect, useRef } from 'react';
import api from '../api';
import PolarsProblem from './problem_types/PolarsProblem';
import CardProblem from './problem_types/CardProblem';
import MultiChoiceProblem from './problem_types/MultiChoiceProblem';
import { Box, Button, Typography } from '@mui/material';

interface Problem {
  problem_type: string;
  problem_id: number;
  //concept_id: number;
  // code_default: string;
  // datasets: string;
  // description?: string;
  // answer: string;
  //hint: string;
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
  const [problemStartTime, setProblemStartTime] = useState<number | null>(null);

  useEffect(() => {
    fetchProblemsRemaining();
    fetchConcept();
  }, []);

  const fetchProblemsRemaining = async () => {
    const response = await api.get('/api/problem/get_number_problems_remaining');
    console.log(response.data.remaining);
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
    if (problem && problemStartTime) {
      const duration = Date.now() - problemStartTime;
      console.log('Duration of problem', duration);
      try {
        await api.post('/api/review', {
          problem_id: problem.problem_id,
          result: result,
          duration_ms: duration,
        });

        fetchConcept();
      } catch (error) {
        console.error('Error submitting review:', error);
      }
    }
  };

  const handleSuspend = async () => {
    try {
      if (problem) {
        await api.post(`/api/problem/suspend/${problem.problem_id}`);
        await fetchConcept();
      }
    } catch (error) {
      console.error('Error suspending:', error);
    }
  };

  const handleBury = async () => {
    try {
      if (problem) {
        await api.post(`/api/problem/bury/${problem.problem_id}`);
        await fetchConcept();
      }
    } catch (error) {
      console.error('Error burying:', error);
    }
  };

  const fetchConcept = async () => {
    fetchProblemsRemaining();
    try {
      const response = await api.get('/api/problem/get_next_problem');
      if (response.data.problems.length === 0) {
        setProblemsRemaining(false);
      } else {
        setProblem(response.data.problems[0]);
        setProblemStartTime(Date.now());
        console.log(response.data);
      }
    } catch (error) {
      console.error('Error fetching concept', error);
    }
  };

  return (
    <>
      <Typography>
        Remaining probs = {numberProblemsRemaining}, Problem type = {problem?.problem_type}
      </Typography>
      {problemsRemaining ? (
        <Box sx={{ maxWidth: 1200, margin: 'auto', mt: 4 }}>
          <Button
            variant="contained"
            onClick={handleSuspend}
            sx={{ mt: 2, backgroundColor: 'red', '&:hover': { backgroundColor: 'darkred' } }}
          >
            Suspend
          </Button>
          <Button
            variant="contained"
            onClick={handleBury}
            sx={{ mt: 2, backgroundColor: 'red', '&:hover': { backgroundColor: 'darkred' } }}
          >
            Bury
          </Button>
          {(problem?.problem_type === 'polars' ||
            problem?.problem_type === 'sql' ||
            problem?.problem_type === 'pyspark') && (
            <>
              <PolarsProblem problem={problem} handleScore={handleScore} />
            </>
          )}
          {problem?.problem_type === 'multi_choice' && (
            <>
              <MultiChoiceProblem problem={problem} handleScore={handleScore} />
            </>
          )}
          {problem?.problem_type === 'card' && (
            <>
              <CardProblem problem={problem} handleScore={handleScore} />
            </>
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
