import React, { useState } from 'react';
import api from '../api';
import Editor from '@monaco-editor/react';
import { Button, CircularProgress, Typography, Box, Alert } from '@mui/material';
import PandasJsonTable from '../components/PandasTable';

const AddCode: React.FC = () => {
  const [datasetPath, setDatasetPath] = useState('');
  const [description, setDescription] = useState('');
  const [code, setCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [submittedResult, setSubmittedResult] = useState<any>(null);

  const handleRunCode = async () => {
    setIsLoading(true);
    try {
      const response = await api.post('/api/code/test_code', {
        code: code,
        dataset_name: datasetPath,
      });
      console.log(response);
      setSubmittedResult(JSON.parse(response.data.result_head));
    } catch (error) {
      console.error('Error executing code:', error);
      alert('Error executing code. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSaveCode = async () => {
    console.log('trying to add card');
    try {
      const response = await api.post('/api/code/add_code', {
        description: description,
        dataset_name: datasetPath,
        code: code,
      });
      console.log('Card added:', response.data);
      setCode('');
      setDescription('');
      setDatasetPath('');
      setSubmittedResult(false);
      alert('Code added successfully!');
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
      <input
        value={datasetPath}
        onChange={(e) => setDatasetPath(e.target.value)}
        placeholder="Dataset path"
        style={{ padding: '10px', fontSize: '16px' }}
      />
      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Description"
        rows={3}
        style={{ padding: '10px', fontSize: '16px' }}
      />
      <Editor
        height="400px"
        defaultLanguage="python"
        value={code}
        onChange={(value) => setCode(value || '')}
        options={{
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          fontSize: 14,
        }}
      />
      <Button variant="contained" color="primary" onClick={handleRunCode} disabled={isLoading}>
        {isLoading ? <CircularProgress size={24} /> : 'Run Code'}
      </Button>
      {submittedResult && (
        <Box sx={{ mt: 4, mb: 4 }}>
          <Typography variant="h5" component="div" gutterBottom>
            Execution Result:
          </Typography>
          <PandasJsonTable data={submittedResult} />
        </Box>
      )}
      {submittedResult && (
        <Box sx={{ mt: 4, mb: 4 }}>
          <Button
            variant="contained"
            color="secondary"
            onClick={handleSaveCode}
            disabled={isLoading}
            sx={{ mt: 2 }}
          >
            Save code problem.
          </Button>
        </Box>
      )}
    </div>
  );
};

export default AddCode;
