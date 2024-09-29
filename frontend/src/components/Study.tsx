import React, { useState, useEffect, useRef } from 'react';
import api from '../api';
import PolarsProblem from './problem_types/PolarsProblem';
import { Box } from '@mui/material';

interface Problem {
  problem_type: string;
  problem_id: number;
  //concept_id: number;
  code_default: string;
  datasets: string;
  description?: string;
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

  useEffect(() => {
    fetchConcept();
  }, []);

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
        await api.post('/api/reviews', {
          problem_id: problem.problem_id,
          result: result,
        });
        fetchConcept();
      } catch (error) {
        console.error('Error submitting review:', error);
      }
    }
  };

  const fetchConcept = async () => {
    try {
      const response = await api.get('/api/get_next_problem');
      console.log(response);
      setProblem(response.data);
    } catch (error) {
      console.error('Error fetching concept', error);
    }
  };

  return (
    <>
      <Box sx={{ maxWidth: 1200, margin: 'auto', mt: 4 }}>
        {problem?.problem_type == 'polars' && (
          <PolarsProblem problem={problem} handleScore={handleScore} />
        )}
      </Box>
    </>
    // <>
    //   {problem?.description && <Description text={problem.description} />}
    //   <Box sx={{ mt: 4, mb: 4 }}></Box>
    //   {problem?.datasets && (
    //     <DatasetRenderer {...{ selectedDataset, setSelectedDataset, datasets: problem.datasets }} />
    //   )}
    // </>
  );
};

export default Study;
