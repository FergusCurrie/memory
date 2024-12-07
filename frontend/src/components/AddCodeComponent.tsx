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
  Autocomplete,
  TextField,
} from '@mui/material';
import PandasJsonTable from './study_components/PandasTable';

const AddCode: React.FC = ({ problemType }) => {
  const [datasetPaths, setDatasetPaths] = useState<string[]>([]);
  const [description, setDescription] = useState('');
  const [code, setCode] = useState('');
  const [preprocessingCode, setPreprocessingCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [submittedResult, setSubmittedResult] = useState<any>(null);

  const [availableDatasets, setAvailableDatasets] = useState<string[]>([]);

  const [tags, setTags] = useState<string[]>([]);

  const [defaultCode, setDefaultCode] = useState('');

  const handleDatasetChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    setDatasetPaths(event.target.value as string[]);
  };

  const handleRemoveDataset = (datasetToRemove: string) => {
    setDatasetPaths((prevDatasets) =>
      prevDatasets.filter((dataset) => dataset !== datasetToRemove),
    );
  };

  // Update handleRunCode to use the problemType
  const handleRunCode = async () => {
    setIsLoading(true);
    try {
      const payload = {
        code: code,
        preprocessing_code: preprocessingCode,
        dataset_names: datasetPaths,
        problem_type: problemType, // Add this line
      };
      console.log(payload);
      const response = await api.post(`/api/code/check_creation_code`, payload);
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
      const response = await api.post('/api/problem', {
        description: description,
        dataset_names: datasetPaths,
        code: code,
        preprocessing_code: preprocessingCode,
        default_code: defaultCode,
        problem_type: problemType, // Add this line
        tags: tags,
      });
      console.log('Card added:', response.data);
      setSubmittedResult(false);
      alert('Code added successfully!');
    } catch (error) {
      console.log(error);
      alert(error);
    }
  };

  useEffect(() => {
    const fetchDatasets = async () => {
      console.log('fetching');
      try {
        const response = await api.get('/api/available_datasets');
        console.log(response);
        setAvailableDatasets(response.data.datasets);
      } catch (error) {
        console.error('Error fetching available datasets:', error);
      }
    };

    fetchDatasets();
  }, []);
  const suggestedTags = ['SQL', 'Polars', 'Data Analysis', 'Aggregation', 'Filtering', 'Joins'];
  return (
    <>
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

      <Autocomplete
        multiple
        freeSolo
        options={suggestedTags}
        value={tags}
        onChange={(event, newValue) => {
          setTags(newValue);
        }}
        renderTags={(value, getTagProps) =>
          value.map((option, index) => (
            <Chip
              {...getTagProps({ index })}
              key={option}
              label={option}
              onDelete={() => {
                setTags(tags.filter((tag) => tag !== option));
              }}
            />
          ))
        }
        renderInput={(params) => (
          <TextField
            {...params}
            variant="outlined"
            label="Tags"
            placeholder="Add tags..."
            fullWidth
            sx={{ mt: 2, mb: 2 }}
          />
        )}
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
    </>
  );
};

export default AddCode;
