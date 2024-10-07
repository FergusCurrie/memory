import React, { useState, useEffect, useRef } from 'react';
import Description from '../study_components/Description';
import DatasetRenderer from '../study_components/DatasetRenderer';
import CodeEditor from '../study_components/CodeEditor';
import NextCardManagement from '../study_components/NextCardManagement';

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

interface PolarsProblem {
  problem: Problem;
  handleScore: (result: boolean) => void;
}

const PolarsProblem: React.FC<PolarsProblem> = ({ problem, handleScore }) => {
  const [selectedDataset, setSelectedDataset] = useState<string>('');
  const [testPassed, setTestPassed] = useState<boolean>(false);

  useEffect(() => {
    if (problem) {
      setSelectedDataset('');
      setTestPassed(false);
      console.log(problem);
    }
  }, [problem]);

  return (
    <>
      <Description text={problem.description} />
      <DatasetRenderer
        {...{ selectedDataset, setSelectedDataset, datasets: JSON.parse(problem.datasets) }}
      />
      <CodeEditor
        {...{
          problem_id: problem?.problem_id,
          testPassed,
          setTestPassed,
          code_default: problem.code_default,
        }}
      />
      <NextCardManagement {...{ testPassed, handleScore, answer: problem.answer }} />
    </>
  );
};

export default PolarsProblem;
