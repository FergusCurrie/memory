import React, { useState, useEffect, useRef } from 'react';
import Description from '../study_components/Description';
import DatasetRenderer from '../study_components/DatasetRenderer';
import CodeEditor from '../study_components/CodeEditor';
import NextCardManagement from '../study_components/NextCardManagement';
import api from '../../api';

interface Problem {
  problem_type: string;
  problem_id: number;
  //concept_id: number;
  // code_default: string;
  // datasets: Record<string, any>;
  // description?: string;
  // answer: string;
  //hint: string;
}

interface PolarsProblemData {
  problem_type: string;
  problem_id: number;
  //concept_id: number;
  code_default: string;
  datasets: Record<string, any>;
  description?: string;
  answer: string;
  //hint: string;
}

interface PolarsProblem {
  problem: Problem;
  handleScore: (result: boolean) => void;
}

const PolarsProblem: React.FC<PolarsProblem> = ({ problem, handleScore }) => {
  const [selectedDataset, setSelectedDataset] = useState<string>('');
  const [testPassed, setTestPassed] = useState<boolean>(false);
  const [polarsProblemData, setPolarsProblemData] = useState<PolarsProblemData>();

  const fetchPolarsProblemData = async () => {
    console.log('fetching polars prbo')
    try {
      const response = await api.get(`/api/problem/data_wrangling/${problem.problem_id}`);
      console.log(response)
      setPolarsProblemData(response.data)
    } catch (error) {
      console.error('Error fetching concept', error);
    }
  };


  useEffect(() => {
    console.log(problem)
    if (problem) {
      fetchPolarsProblemData()
      setSelectedDataset('');
      setTestPassed(false);
    }
  }, [problem]);

  return (
    <>
      <Description text={polarsProblemData?.description} />
      <DatasetRenderer
        {...{ selectedDataset, setSelectedDataset, datasets: polarsProblemData?.datasets }}
      />
      <CodeEditor
        {...{
          problem_id: polarsProblemData?.problem_id,
          testPassed,
          setTestPassed,
          code_default: polarsProblemData?.code_default,
        }}
      />
      <NextCardManagement {...{ testPassed, handleScore, answer: polarsProblemData?.answer }} />
    </>
  );
};

export default PolarsProblem;
