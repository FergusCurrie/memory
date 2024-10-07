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

interface CodeCard {
  problem_id: number;
  dataset_name: string;
  dataset_headers: string;
  code: string;
  default_code: string;
  preprocessing_code: string;
  description: string;
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

  const handleSaveEdit = async () => {
    if (editingCard) {
      try {
        await api.put(`/api/code/${editingCard.problem_id}`, editingCard);
        setCodeCards(
          codeCards.map((c) => (c.problem_id === editingCard.problem_id ? editingCard : c)),
        );
        setEditingCard(null);
      } catch (error) {
        console.error('Error updating code card:', error);
      }
    }
  };

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

      <Dialog open={!!editingCard} onClose={() => setEditingCard(null)}>
        <DialogTitle>Edit Code Card</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Dataset Name"
            fullWidth
            value={editingCard?.dataset_name || ''}
            onChange={(e) => setEditingCard((prev) => ({ ...prev!, dataset_name: e.target.value }))}
          />
          <TextField
            margin="dense"
            label="Problem Description"
            fullWidth
            multiline
            rows={4}
            value={editingCard?.description || ''}
            onChange={(e) =>
              setEditingCard((prev) => ({ ...prev!, problem_description: e.target.value }))
            }
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
      </Dialog>
    </Box>
  );
};

export default BrowseCodeCards;
