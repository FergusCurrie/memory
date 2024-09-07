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
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import api from '../api';

interface Card {
  id: number;
  question: string;
  answer: string;
}

interface Review {
  id: number;
  card_id: number;
  result: boolean;
  created_at: string;
}

const BrowseCards: React.FC = () => {
  const [cards, setCards] = useState<Card[]>([]);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [selectedCardId, setSelectedCardId] = useState<number | null>(null);

  useEffect(() => {
    fetchCards();
    fetchReviews();
  }, []);

  const fetchCards = async () => {
    try {
      const response = await api.get('/api/cards');
      setCards(response.data.cards);
    } catch (error) {
      console.error('Error fetching cards:', error);
    }
  };

  const fetchReviews = async () => {
    try {
      const response = await api.get('/api/reviews');
      setReviews(response.data.reviews);
    } catch (error) {
      console.error('Error fetching reviews:', error);
    }
  };

  const handleCardClick = (cardId: number) => {
    setSelectedCardId(cardId === selectedCardId ? null : cardId);
  };

  const handleDeleteCard = async (cardId: number, event: React.MouseEvent) => {
    event.stopPropagation(); // Prevent row click event
    if (
      window.confirm(
        'Are you sure you want to delete this card? This will also delete all related reviews.',
      )
    ) {
      try {
        await api.delete(`/api/cards/${cardId}`);
        setCards(cards.filter((card) => card.id !== cardId));
        setReviews(reviews.filter((review) => review.card_id !== cardId));
        if (selectedCardId === cardId) {
          setSelectedCardId(null);
        }
      } catch (error) {
        console.error('Error deleting card:', error);
      }
    }
  };

  const filteredReviews = selectedCardId
    ? reviews.filter((review) => review.card_id === selectedCardId)
    : reviews;

  return (
    <Box sx={{ maxWidth: 1200, margin: 'auto', mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Browse Cards
      </Typography>
      <TableContainer component={Paper} sx={{ mb: 4 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Question</TableCell>
              <TableCell>Answer</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {cards.map((card) => (
              <TableRow
                key={card.id}
                onClick={() => handleCardClick(card.id)}
                sx={{
                  cursor: 'pointer',
                  backgroundColor: card.id === selectedCardId ? '#e3f2fd' : 'inherit',
                  '&:hover': { backgroundColor: '#f5f5f5' },
                }}
              >
                <TableCell>{card.id}</TableCell>
                <TableCell>{card.question}</TableCell>
                <TableCell>{card.answer}</TableCell>
                <TableCell>
                  <IconButton onClick={(e) => handleDeleteCard(card.id, e)} color="error">
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Typography variant="h4" gutterBottom>
        Review History
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
              <TableCell>Card ID</TableCell>
              <TableCell>Result</TableCell>
              <TableCell>Timestamp</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredReviews.map((review) => (
              <TableRow key={review.id}>
                <TableCell>{review.id}</TableCell>
                <TableCell>{review.card_id}</TableCell>
                <TableCell>{review.result ? 'Correct' : 'Incorrect'}</TableCell>
                <TableCell>
                  {(() => {
                    console.log('Review date:', review.created_at);
                    if (!review.created_at) {
                      return 'No date available';
                    }
                    const date = new Date(review.created_at);
                    console.log('Parsed date:', date);
                    return date.toString() !== 'Invalid Date'
                      ? date.toLocaleString()
                      : `Invalid Date: ${review.created_at}`;
                  })()}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default BrowseCards;
