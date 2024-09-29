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

const AddCode: React.FC = () => {
  // Change datasetPath to datasetPaths and make it an array
  const [datasetPaths, setDatasetPaths] = useState<string[]>([]);
  const [description, setDescription] = useState('');
  const [code, setCode] = useState('');
  const [preprocessingCode, setPreprocessingCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [submittedResult, setSubmittedResult] = useState<any>(null);

  const [availableDatasets, setAvailableDatasets] = useState<string[]>([]);

  const [defaultCode, setDefaultCode] = useState('');

  useEffect(() => {
    const fetchDatasets = async () => {
      try {
        const response = await api.get('/api/code/available_datasets');
        setAvailableDatasets(response.data.datasets);
      } catch (error) {
        console.error('Error fetching available datasets:', error);
      }
    };

    fetchDatasets();
  }, []);

  const handleDatasetChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    setDatasetPaths(event.target.value as string[]);
  };

  const handleRemoveDataset = (datasetToRemove: string) => {
    setDatasetPaths((prevDatasets) =>
      prevDatasets.filter((dataset) => dataset !== datasetToRemove),
    );
  };

  // Update handleRunCode and handleSaveCode to use datasetPaths instead of datasetPath
  const handleRunCode = async () => {
    setIsLoading(true);
    try {
      const response = await api.post('/api/code/test_code', {
        code: code,
        preprocessing_code: preprocessingCode,
        dataset_names: datasetPaths, // Changed to datasetPaths
      });
      console.log(response);
      setSubmittedResult(JSON.parse(response.data.result_head));
    } catch (error) {
      console.error('Error executing code:', error);
      alert('Error executing code. Please try again.', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSaveCode = async () => {
    console.log('trying to add card');
    try {
      const response = await api.post('/api/code/add_code', {
        description: description,
        dataset_names: datasetPaths,
        code: code,
        preprocessing_code: preprocessingCode,
        default_code: defaultCode, // Add this line
      });
      console.log('Card added:', response.data);
      // setCode('');
      // setPreprocessingCode('');
      // setDescription('');
      // setDatasetPaths([]);
      // setDefaultCode(''); // Reset default code
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
      <FormControl fullWidth>
        <InputLabel id="dataset-select-label">Datasets</InputLabel>
        <Select
          labelId="dataset-select-label"
          id="dataset-select"
          multiple
          value={datasetPaths}
          onChange={handleDatasetChange}
          style={{ fontSize: '16px' }}
          renderValue={(selected) => (
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
              {(selected as string[]).map((value) => (
                <Chip
                  key={value}
                  label={value}
                  onDelete={() => handleRemoveDataset(value)}
                  onMouseDown={(event) => {
                    event.stopPropagation();
                  }}
                />
              ))}
            </Box>
          )}
        >
          {availableDatasets.map((dataset) => (
            <MenuItem key={dataset} value={dataset}>
              {dataset}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Description"
        rows={3}
        style={{ padding: '10px', fontSize: '16px' }}
      />
      <Typography variant="h6">Default Code</Typography>
      <Editor
        height="200px"
        defaultLanguage="python"
        value={defaultCode}
        onChange={(value) => setDefaultCode(value || '')}
        options={{
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          fontSize: 14,
        }}
      />
      <Typography variant="h6">Preprocessing Code</Typography>
      <Editor
        height="200px"
        defaultLanguage="python"
        value={preprocessingCode}
        onChange={(value) => setPreprocessingCode(value || '')}
        options={{
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          fontSize: 14,
        }}
      />
      <Typography variant="h6">Main Code</Typography>
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
