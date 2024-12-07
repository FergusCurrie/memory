import React, { useEffect, useState } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Box,
  Button,
  IconButton,
  TextField,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import api from '../api';
import PauseIcon from '@mui/icons-material/Pause';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
// Add these new imports
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import HourglassEmptyIcon from '@mui/icons-material/HourglassEmpty';
import HelpIcon from '@mui/icons-material/Help';
import EditProblemDialog from '../components/EditProblemDialog';

interface CodeCard {
  problem_id: number;
  dataset_name: string;
  dataset_headers: string;
  code: string;
  default_code: string;
  preprocessing_code: string;
  description: string;
  is_suspended: boolean;
}
interface EditProblemData {
  description: string;
  code_default: string;
  answer: string;
}

interface CodeReview {
  id: number;
  problem_id: number;
  result: boolean;
  date_created: string;
}

const BrowseCodeCards: React.FC = () => {
  const [codeCards, setCodeCards] = useState<CodeCard[]>([]);
  const [codeReviews, setCodeReviews] = useState<CodeReview[]>([]);
  const [selectedCardId, setSelectedCardId] = useState<number | null>(null);
  const [editingCard, setEditingCard] = useState<CodeCard | null>(null);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);

  useEffect(() => {
    fetchCodeCards();
    fetchCodeReviews();
  }, []);

  const fetchCodeCards = async () => {
    try {
      const response = await api.get('/api/problem/');
      console.log(response);
      setCodeCards(response.data);
    } catch (error) {
      console.error('Error fetching code cards:', error);
    }
  };

  const fetchCodeReviews = async () => {
    try {
      const response = await api.get('/api/review');
      console.log('x', response);
      setCodeReviews(response.data);
    } catch (error) {
      console.error('Error fetching code reviews:', error);
    }
  };

  const handleCardClick = (cardId: number) => {
    setSelectedCardId(cardId === selectedCardId ? null : cardId);
  };

  const handleEditCard = (card: CodeCard) => {
    setEditingCard(card);
  };

  const handleSaveEdit = async (editedData: EditProblemData) => {
    if (editingCard) {
      try {
        await api.put(`/api/problem/${editingCard.problem_id}`, {
          description: editedData.description,
          default_code: editedData.code_default,
          code: editedData.answer,
        });
        setCodeCards(
          codeCards.map((c) =>
            c.problem_id === editingCard.problem_id
              ? { ...c, description: editedData.description }
              : c,
          ),
        );
        setEditingCard(null);
      } catch (error) {
        console.error('Error updating code card:', error);
      }
    }
  };

  // const handleSaveEdit = async () => {
  //   if (editingCard) {
  //     console.log('Saving edit');
  //     try {
  //       await api.put(`/api/problem/${editingCard.problem_id}`, {
  //         description: editingCard.description,
  //         code: editingCard.code,
  //         default_code: editingCard.default_code,
  //       });
  //       setCodeCards(
  //         codeCards.map((c) => (c.problem_id === editingCard.problem_id ? editingCard : c)),
  //       );
  //       setEditingCard(null);
  //     } catch (error) {
  //       console.error('Error updating code card:', error);
  //     }
  //   }
  // };

  const handleDeleteReview = async (reviewId: number, event: React.MouseEvent) => {
    event.stopPropagation();
    if (window.confirm('Are you sure you want to delete this review?')) {
      try {
        await api.delete(`/api/review/${reviewId}`);
        setCodeReviews(codeReviews.filter((review) => review.id !== reviewId));
      } catch (error) {
        console.error('Error deleting review:', error);
      }
    }
  };

  const handleDeleteCode = async (problem_id: number, event: React.MouseEvent) => {
    event.stopPropagation();
    if (window.confirm('Are you sure you want to delete this review?')) {
      try {
        await api.delete(`/api/problem/${problem_id}`);
        setCodeReviews(codeReviews.filter((review) => review.problem_id !== problem_id));
      } catch (error) {
        console.error('Error deleting review:', error);
      }
    }
  };

  const handleToggleSuspend = async (problem_id: number, event: React.MouseEvent) => {
    event.stopPropagation();
    try {
      await api.post(`/api/problem/suspend/${problem_id}`);
      setCodeCards(
        codeCards.map((card) =>
          card.problem_id === problem_id ? { ...card, is_suspended: !card.is_suspended } : card,
        ),
      );
    } catch (error) {
      console.error('Error toggling suspend status:', error);
    }
  };

  const filteredReviews = selectedCardId
    ? codeReviews.filter((review) => review.problem_id === selectedCardId)
    : codeReviews;

  return (
    <Box sx={{ maxWidth: 1200, margin: 'auto', mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Browse Code Cards
      </Typography>
      <TableContainer component={Paper} sx={{ mb: 4 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Dataset Name</TableCell>
              <TableCell>Problem Description</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {(codeCards || []).map((card) => (
              <TableRow
                key={card.problem_id}
                onClick={() => handleCardClick(card.problem_id)}
                sx={{
                  cursor: 'pointer',
                  backgroundColor: card.problem_id === selectedCardId ? '#e3f2fd' : 'inherit',
                  '&:hover': { backgroundColor: '#f5f5f5' },
                }}
              >
                <TableCell>{card.problem_id}</TableCell>
                <TableCell>{card.dataset_name}</TableCell>
                <TableCell>{card.description}</TableCell>
                <TableCell>
                  <IconButton onClick={(e) => handleDeleteCode(card.problem_id, e)} color="error">
                    <DeleteIcon />
                  </IconButton>
                  <IconButton onClick={() => handleEditCard(card)} color="primary">
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    onClick={(e) => handleToggleSuspend(card.problem_id, e)}
                    color={card.is_suspended ? 'warning' : 'success'}
                  >
                    {card.is_suspended ? <PlayArrowIcon /> : <PauseIcon />}
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Typography variant="h4" gutterBottom>
        Code Review History
        {selectedCardId && (
          <Button onClick={() => setSelectedCardId(null)} sx={{ ml: 2 }} variant="outlined">
            Clear Filter
          </Button>
        )}
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Code Card ID</TableCell>
              <TableCell>Result</TableCell>
              <TableCell>Timestamp</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {(filteredReviews || []).map((review) => (
              <TableRow key={review.id}>
                <TableCell>{review.id}</TableCell>
                <TableCell>{review.problem_id}</TableCell>
                <TableCell>{review.result ? 'Correct' : 'Incorrect'}</TableCell>
                <TableCell>
                  {(() => {
                    if (!review.date_created) {
                      return 'No date available';
                    }
                    const date = new Date(review.date_created);
                    return date.toString() !== 'Invalid Date'
                      ? date.toLocaleString()
                      : `Invalid Date: ${review.date_created}`;
                  })()}
                </TableCell>
                <TableCell>
                  <IconButton onClick={(e) => handleDeleteReview(review.id, e)} color="error">
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <EditProblemDialog
        open={!!editingCard}
        onClose={() => setEditingCard(null)}
        onSave={handleSaveEdit}
        initialData={
          editingCard
            ? {
                description: editingCard.description,
                code_default: editingCard.default_code,
                answer: editingCard.code,
              }
            : null
        }
      />
      {/* <Dialog open={!!editingCard} onClose={() => setEditingCard(null)}>
        <DialogTitle>Edit Code Card</DialogTitle>
        <DialogContent>
          <TextField
            margin="dense"
            label="Dataset Name"
            fullWidth
            value={editingCard?.dataset_name || ''}
            InputProps={{
              readOnly: true,
            }}
          />
          <TextField
            margin="dense"
            label="Problem Description"
            fullWidth
            multiline
            rows={4}
            value={editingCard?.description || ''}
            onChange={(e) => setEditingCard((prev) => ({ ...prev!, description: e.target.value }))}
          />
          <TextField
            margin="dense"
            label="Default Code"
            fullWidth
            multiline
            rows={4}
            value={editingCard?.default_code || ''}
            onChange={(e) => setEditingCard((prev) => ({ ...prev!, default_code: e.target.value }))}
          />
          <TextField
            margin="dense"
            label="Code"
            fullWidth
            multiline
            rows={6}
            value={editingCard?.code || ''}
            onChange={(e) => setEditingCard((prev) => ({ ...prev!, code: e.target.value }))}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditingCard(null)}>Cancel</Button>
          <Button onClick={handleSaveEdit}>Save</Button>
        </DialogActions>
      </Dialog> */}
    </Box>
  );
};

export default BrowseCodeCards;
