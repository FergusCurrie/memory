import React, { useState, useEffect, useRef } from 'react';
import Description from '../study_components/Description';
import DatasetRenderer from '../study_components/DatasetRenderer';
import CodeEditor from '../study_components/CodeEditor';
import NextCardManagement from '../study_components/NextCardManagement';
import api from '../../api';
import EditProblemDialog from '../EditProblemDialog';
import { IconButton } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
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
interface EditProblemData {
  description: string;
  code_default: string;
  answer: string;
}

const PolarsProblem: React.FC<PolarsProblem> = ({ problem, handleScore }) => {
  const [selectedDataset, setSelectedDataset] = useState<string>('');
  const [testPassed, setTestPassed] = useState<boolean>(false);
  const [polarsProblemData, setPolarsProblemData] = useState<PolarsProblemData>();
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);

  const fetchPolarsProblemData = async () => {
    console.log('fetching polars prbo');
    try {
      console.log('hello');
      const response = await api.get(`/api/problem/data_wrangling/${problem.problem_id}`);
      console.log('response:');
      console.log(response.data['problems'][0]);
      setPolarsProblemData(response.data['problems'][0]);
    } catch (error) {
      console.error('Error fetching concept', error);
    }
  };

  const handleSaveEdit = async (editedData: EditProblemData) => {
    if (polarsProblemData) {
      try {
        await api.put(`/api/problem/${polarsProblemData.problem_id}`, {
          description: editedData.description,
          default_code: editedData.code_default,
          code: editedData.answer,
        });
        setPolarsProblemData({
          problem_type: polarsProblemData.problem_type,
          problem_id: polarsProblemData.problem_id,
          code_default: editedData.code_default,
          datasets: polarsProblemData.datasets,
          description: editedData.description,
          answer: editedData.answer,
        });
        setIsEditDialogOpen(false);
      } catch (error) {
        console.error('Error updating code card:', error);
      }
    }
  };

  const handleEditCard = () => {
    setIsEditDialogOpen(true);
  };

  useEffect(() => {
    console.log(problem);
    if (problem) {
      fetchPolarsProblemData();
      setSelectedDataset('');
      setTestPassed(false);
    }
  }, [problem]);

  return (
    <>
      <IconButton onClick={() => handleEditCard()} color="primary">
        <EditIcon />
      </IconButton>
      <EditProblemDialog
        open={!!isEditDialogOpen}
        onClose={() => setIsEditDialogOpen(false)}
        onSave={handleSaveEdit}
        initialData={
          isEditDialogOpen && polarsProblemData
            ? {
                description: polarsProblemData.description || '',
                code_default: polarsProblemData.code_default || '',
                answer: polarsProblemData.answer || '',
              }
            : null
        }
      />
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
