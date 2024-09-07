import React, { useState, useEffect } from 'react';
import { Button, Card, CardContent, Typography, Box, Paper } from '@mui/material';
import api from '../api';

interface FlashCard {
  id: number;
  question: string;
  answer: string;
}

const Study: React.FC = () => {
  const [cards, setCards] = useState<FlashCard[]>([]);
  const [currentCard, setCurrentCard] = useState<FlashCard | null>(null);
  const [showAnswer, setShowAnswer] = useState(false);

  useEffect(() => {
    fetchCards();
  }, []);

  const fetchCards = async () => {
    try {
      const response = await api.get('/api/cards_to_review');
      console.log(response);
      setCards(response.data.cards);
      pickRandomCard(response.data.cards);
    } catch (error) {
      console.error('Error fetching cards:', error);
    }
  };

  const pickRandomCard = (cardArray: FlashCard[]) => {
    if (cardArray.length > 0) {
      const randomIndex = Math.floor(Math.random() * cardArray.length);
      setCurrentCard(cardArray[randomIndex]);
      setShowAnswer(false);
    } else {
      // Handle the case when there are no more cards to review
      setCurrentCard(null);
    }
  };

  const handleReveal = () => {
    setShowAnswer(true);
  };

  const handleScore = async (result: boolean) => {
    if (currentCard) {
      try {
        await api.post('/api/reviews', {
          card_id: currentCard.id,
          result: result,
        });

        // Remove the current card from the cards array
        setCards((prevCards) => prevCards.filter((card) => card.id !== currentCard.id));

        // Pick a random card from the updated list
        pickRandomCard(cards.filter((card) => card.id !== currentCard.id));
      } catch (error) {
        console.error('Error submitting review:', error);
      }
    }
  };

  if (!currentCard) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <Paper elevation={3} sx={{ p: 3, maxWidth: 400 }}>
          <Typography variant="h6" align="center">
            All done!
          </Typography>
        </Paper>
      </Box>
    );
  }

  return (
    <Box sx={{ maxWidth: 600, margin: 'auto', mt: 4 }}>
      <Card>
        <CardContent>
          <Typography variant="h5" component="div" gutterBottom>
            Question:
          </Typography>
          <Typography variant="body1" paragraph>
            {currentCard.question}
          </Typography>
          {showAnswer && (
            <>
              <Typography variant="h5" component="div" gutterBottom>
                Answer:
              </Typography>
              <Typography variant="body1" paragraph>
                {currentCard.answer}
              </Typography>
            </>
          )}
        </CardContent>
      </Card>
      <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-between' }}>
        {!showAnswer ? (
          <Button variant="contained" onClick={handleReveal} fullWidth>
            Reveal Answer
          </Button>
        ) : (
          <>
            <Button
              variant="contained"
              color="success"
              onClick={() => handleScore(true)}
              sx={{ flex: 1, mr: 1 }}
            >
              Correct
            </Button>
            <Button
              variant="contained"
              color="error"
              onClick={() => handleScore(false)}
              sx={{ flex: 1, ml: 1 }}
            >
              Incorrect
            </Button>
          </>
        )}
      </Box>
    </Box>
  );
};

export default Study;
