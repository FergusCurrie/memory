import React, { useState, useEffect, useRef } from 'react';
import {
  Button,
  Card,
  CardContent,
  Typography,
  Box,
  Table,
  TableHead,
  TableCell,
  TableRow,
  TableContainer,
  TableBody,
  Paper,
  CircularProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import api from '../api';
import Editor, { OnMount } from '@monaco-editor/react';
import PandasJsonTable from './study_components/PandasTable';
import { KeyboardEvent } from 'react';
import { FormControl, InputLabel, Select, MenuItem } from '@mui/material';
// import Description from './study_components/Description';
// import DatasetRenderer from './study_components/DatasetRenderer';
import PolarsProblem from './problem_types/PolarsProblem';
// interface CodeCard {
//   id: number;
//   note_id: number;
//   dataset_name: string;
//   problem_description: string;
//   code: string;
//   dataset_headers: string; // This is now a JSON string containing multiple datasets
//   code_start: string;
// }

// const selectRandomConcept = (concepts) => {
//     const randomIndex = Math.floor(Math.random() * concepts.length);
//     const nextConcept = concepts[randomIndex];
//     setCurrentConcept(nextConcept);
//   };

interface Problem {
  problem_type: string;
  problem_id?: number;
  concept_id?: number;
  code_default?: string;
  datasets?: Array<string>;
  description?: string;
  hint?: string;
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
        // Fetch a new problem after submitting the review

        //setCards((prevCards) => prevCards.filter((card) => card.id !== currentCard.id));
        //pickRandomCard(cards.filter((card) => card.id !== currentCard.id));
        //setCodeError('');
        //setSubmittedResult(null);
        //setTestPassed(null);
        fetchConcept();
      } catch (error) {
        console.error('Error submitting review:', error);
      }
    }
  };

  const fetchConcept = async () => {
    try {
      const response = await api.get('/api/get_next_problem');
      //console.log(response);
      setProblem(response.data.problem);

      //selectRandomConcept(response.data.codes);
    } catch (error) {
      console.error('Error fetching concept', error);
    }
  };

  return (
    <>
      {problem?.problem_type == 'polars' && (
        <PolarsProblem problem={problem} handleScore={handleScore} />
      )}
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
