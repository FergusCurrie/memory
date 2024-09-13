import React, { useState, useEffect } from 'react';
import { Button, Card, CardContent, Typography, Box } from '@mui/material';
import api from '../api';

interface BasicCard {
  id: number;
  question: string;
  answer: string;
}

const StudyBasic: React.FC = () => {
  const [cards, setCards] = useState<BasicCard[]>([]);
  const [currentCard, setCurrentCard] = useState<BasicCard | null>(null);
  const [showAnswer, setShowAnswer] = useState(false);

  useEffect(() => {
    fetchCards();
  }, []);

  const fetchCards = async () => {
    try {
      const response = await api.get('/api/card/cards_to_review');
      setCards(response.data.cards);
      pickRandomCard(response.data.cards);
    } catch (error) {
      console.error('Error fetching basic cards:', error);
    }
  };

  const pickRandomCard = (cardArray: BasicCard[]) => {
    if (cardArray.length > 0) {
      const randomIndex = Math.floor(Math.random() * cardArray.length);
      setCurrentCard(cardArray[randomIndex]);
      setShowAnswer(false);
    } else {
      setCurrentCard(null);
    }
  };

  const handleScore = async (result: boolean) => {
    if (currentCard) {
      try {
        await api.post('/api/card/reviews', {
          card_id: currentCard.id,
          result: result,
        });
        setCards((prevCards) => prevCards.filter((card) => card.id !== currentCard.id));
        pickRandomCard(cards.filter((card) => card.id !== currentCard.id));
      } catch (error) {
        console.error('Error submitting review:', error);
      }
    }
  };

  if (!currentCard) {
    return <Typography>All done with basic cards!</Typography>;
  }

  return (
    <>
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
          <Button variant="contained" onClick={() => setShowAnswer(true)} fullWidth>
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
    </>
  );
};

export default StudyBasic;
