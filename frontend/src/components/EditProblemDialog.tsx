import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Autocomplete,
  Chip,
} from '@mui/material';

interface EditProblemData {
  description: string;
  code_default: string;
  answer: string;
  tags: string[];
}

interface EditProblemDialogProps {
  open: boolean;
  onClose: () => void;
  onSave: (problemData: EditProblemData) => Promise<void>;
  initialData: EditProblemData | null;
}

const EditProblemDialog: React.FC<EditProblemDialogProps> = ({
  open,
  onClose,
  onSave,
  initialData,
}) => {
  const [editingData, setEditingData] = React.useState<EditProblemData | null>(initialData);

  React.useEffect(() => {
    setEditingData(initialData);
  }, [initialData]);

  const handleSave = async () => {
    if (editingData) {
      await onSave(editingData);
      onClose();
    }
  };

  // Add suggested tags (you might want to pass these as props instead)
  const suggestedTags = ['javascript', 'python', 'react', 'typescript', 'algorithms'];

  if (!editingData) return null;

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Edit Problem</DialogTitle>
      <DialogContent>
        <TextField
          margin="dense"
          label="Problem Description"
          fullWidth
          multiline
          rows={4}
          value={editingData.description}
          onChange={(e) => setEditingData((prev) => ({ ...prev!, description: e.target.value }))}
        />
        <TextField
          margin="dense"
          label="Default Code"
          fullWidth
          multiline
          rows={4}
          value={editingData.code_default}
          onChange={(e) => setEditingData((prev) => ({ ...prev!, code_default: e.target.value }))}
        />
        <TextField
          margin="dense"
          label="Answer"
          fullWidth
          multiline
          rows={6}
          value={editingData.answer}
          onChange={(e) => setEditingData((prev) => ({ ...prev!, answer: e.target.value }))}
        />
        <Autocomplete
          multiple
          freeSolo
          options={suggestedTags}
          value={editingData.tags}
          onChange={(event, newValue) => {
            setEditingData((prev) => ({ ...prev!, tags: newValue }));
          }}
          renderTags={(value, getTagProps) =>
            value.map((option, index) => (
              <Chip
                {...getTagProps({ index })}
                key={option}
                label={option}
                onDelete={() => {
                  setEditingData((prev) => ({
                    ...prev!,
                    tags: prev!.tags.filter((tag) => tag !== option),
                  }));
                }}
              />
            ))
          }
          renderInput={(params) => (
            <TextField
              {...params}
              margin="dense"
              label="Tags"
              placeholder="Add tags..."
              fullWidth
            />
          )}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSave}>Save</Button>
      </DialogActions>
    </Dialog>
  );
};

export default EditProblemDialog;
