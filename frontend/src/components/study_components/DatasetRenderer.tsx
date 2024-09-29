import {
  Card,
  CardContent,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Typography,
} from '@mui/material';
import React, { useState, useEffect, useRef } from 'react';
import PandasJsonTable from './PandasTable';

interface DatasetRendererProps {
  selectedDataset?: string;
  setSelectedDataset: React.Dispatch<React.SetStateAction<string>>;
  datasets?: Array<string>;
}
const DatasetRenderer: React.FC<DatasetRendererProps> = ({
  selectedDataset,
  setSelectedDataset,
  datasets,
}) => {
  return (
    <>
      <FormControl fullWidth sx={{ mt: 4, mb: 2 }}>
        <InputLabel id="dataset-select-label">Select Dataset</InputLabel>
        <Select
          labelId="dataset-select-label"
          id="dataset-select"
          value={selectedDataset}
          label="Select Dataset"
          onChange={(e) => setSelectedDataset(e.target.value as string)}
        >
          {datasets &&
            Object.keys(datasets).map((datasetName) => (
              <MenuItem key={datasetName} value={datasetName}>
                {datasetName}
              </MenuItem>
            ))}
        </Select>
      </FormControl>
      {selectedDataset && datasets && <PandasJsonTable data={datasets[selectedDataset]} />}
    </>
  );
};

export default DatasetRenderer;
