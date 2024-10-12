import React, { useState, useEffect } from 'react';
import api from '../api';
import Editor from '@monaco-editor/react';
import {
  Button,
  CircularProgress,
  Typography,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
} from '@mui/material';
import PandasJsonTable from '../components/study_components/PandasTable';
import AddCode from '../components/AddCodeComponent'

const Add: React.FC = () => {
  // Change datasetPath to datasetPaths and make it an array
  const [problemType, setProblemType] = useState<'polars' | 'pyspark'| 'sql'>('polars');
  const [front, setFront] = useState('');
  const [back, setBack] = useState('');
  useEffect(() => {
  }, []);

  

  const handleProblemTypeChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    setProblemType(event.target.value as 'polars' | 'pyspark' | 'sql');
  };

  const handleSaveCard = async () => {
    console.log('trying to add card');
    try {
      const response = await api.post('/api/problem/card/create', {
        front: front,
        back: back
      });
      console.log('Card added:', response.data);
      setFront('');
      setBack('');
      alert('Card added successfully!');
    } catch (error) {
      console.log(error);
      alert(error);
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '20px',
        maxWidth: '800px',
        margin: 'auto',
      }}
    >
      <h1>Add and Run Code</h1>
      <FormControl fullWidth>
        <InputLabel id="problem-type-select-label">Problem Type</InputLabel>
        <Select
          labelId="problem-type-select-label"
          id="problem-type-select"
          value={problemType}
          onChange={handleProblemTypeChange}
          style={{ fontSize: '16px' }}
        >
          <MenuItem value="polars">Polars</MenuItem>
          <MenuItem value="pyspark">PySpark</MenuItem>
          <MenuItem value="sql">SQL</MenuItem>
          <MenuItem value="card">Card</MenuItem>
        </Select>
      </FormControl>
      {(problemType === 'polars' || problemType === 'pyspark'  || problemType === 'sql' )  && (
        <AddCode problemType={problemType} />
      )}
      { (problemType === 'card') && (
        <>
        <textarea
          value={front}
          onChange={(e) => setFront(e.target.value)}
          placeholder="Front"
          rows={3}
          style={{ padding: '10px', fontSize: '16px' }}
        />
      <textarea
        value={back}
        onChange={(e) => setBack(e.target.value)}
        placeholder="Back"
        rows={3}
        style={{ padding: '10px', fontSize: '16px' }}
      />
       <Button
            variant="contained"
            color="secondary"
            onClick={handleSaveCard}
            // disabled={isLoading}
            sx={{ mt: 2 }}
          >
            Save
          </Button>
      </>
      )}
    </div>
  );
};

export default Add;
