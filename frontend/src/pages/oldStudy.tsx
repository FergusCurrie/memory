import React, { useEffect, useState } from 'react';
import { Box, Button, Divider, Paper, Typography } from '@mui/material';
import api from '../api';
import { InlineMath, BlockMath } from 'react-katex';
import 'katex/dist/katex.min.css';

interface LatexElement {
  type: 'latex' | 'text';
  content: string;
}

interface RenderTextWithLatexProps {
  text: string;
}

const postResult = async (id: string, correct: boolean) => {
  var data = JSON.stringify({
    card: id,
    result: correct,
  });
  console.log(data);
  try {
    const res = await api.post('/api/flashcard/put_result/', data, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (error) {
    alert(error);
  }
};

function processLatexString(text: string): LatexElement[] {
  // Split the text at each instance of \( or \), keeping the delimiters and subsequent text
  const parts = text.split(/(\\\(|\\\))/);
  const elements: LatexElement[] = [];
  let inMathBlock = false;

  parts.forEach((part) => {
    if (part === '\\(') {
      inMathBlock = true;
    } else if (part === '\\)') {
      inMathBlock = false;
    } else {
      if (inMathBlock) {
        // If in a LaTeX block, wrap this part in an object to indicate it is LaTeX
        elements.push({ type: 'latex', content: part });
      } else {
        // Otherwise, treat this part as normal text
        elements.push({ type: 'text', content: part });
      }
    }
  });

  return elements;
}

const RenderTextWithLatex: React.FC<RenderTextWithLatexProps> = ({ text }) => {
  const elements = processLatexString(text);

  return (
    <div>
      {elements.map((el, index) =>
        el.type === 'latex' ? (
          <InlineMath key={index} math={el.content} />
        ) : (
          <span key={index}>{el.content}</span>
        ),
      )}
    </div>
  );
};

const Study = () => {
  const [data, setData] = useState([]);
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);

  const query = async () => {
    try {
      const response = await api.get('/api/cards/');
      console.log(response);
      setData(response.data);
    } catch (error) {
      alert(error);
      console.log(error);
    }
  };

  useEffect(() => {
    query();
  }, []);

  const handleCorrect = () => {
    postResult(data[currentCardIndex].id, true);
    setShowAnswer(false); // Hide answer when moving to the next card
    setCurrentCardIndex((prevIndex) => prevIndex + 1); // Cycle through cards
  };

  const handleIncorrect = () => {
    postResult(data[currentCardIndex].id, false);
    setShowAnswer(false); // Hide answer when moving to the next card
    setCurrentCardIndex((prevIndex) => prevIndex + 1); // Cycle through cards
  };

  const handleShowAnswer = () => {
    setShowAnswer(true);
  };

  return (
    <div>
      {data.length > 0 && currentCardIndex >= 0 && currentCardIndex < data.length ? (
        <div>
          <Box sx={{ backgroundColor: 'background.default', padding: 2 }}>
            {data.length > 0 ? (
              <>
                <Box
                  sx={{
                    display: 'flex',
                    flexDirection: 'column', // Stacks children vertically
                    justifyContent: 'center', // Centers vertically
                    height: '30vh', // Full viewport height to enable vertical centering
                    alignItems: 'center', // Centers horizontally
                    backgroundColor: 'background.default',
                    padding: 2,
                  }}
                >
                  <Paper
                    elevation={3}
                    sx={{
                      alignItems: 'center',
                      p: '5',
                      display: 'flex',
                      flexDirection: 'column',
                      justifyContent: 'center',
                      width: '80%',
                      gap: 2,
                    }}
                  >
                    <Box sx={{ width: '100%', textAlign: 'center', pt: 2, pb: 2 }}>
                      <Typography variant="h5" component="h2">
                        <RenderTextWithLatex text={data[currentCardIndex].question} />
                      </Typography>
                    </Box>
                    <Divider variant="middle" sx={{ width: '80%', my: 2, borderColor: '#000' }} />
                    {/* Horizontal line */}
                    <Box sx={{ width: '100%', textAlign: 'center', pb: 2 }}>
                      <Typography variant="h5" component="h2">
                        {showAnswer && <RenderTextWithLatex text={data[currentCardIndex].answer} />}
                      </Typography>
                    </Box>
                  </Paper>
                </Box>
                {!showAnswer && (
                  <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2, mb: 4 }}>
                    <Button onClick={handleShowAnswer} variant="contained" color="primary">
                      Show Answer
                    </Button>
                  </Box>
                )}

                {showAnswer && (
                  <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2, mb: 4 }}>
                    <Button
                      onClick={handleIncorrect}
                      variant="contained"
                      color="secondary"
                      sx={{ marginLeft: 1, backgroundColor: 'red' }}
                    >
                      Incorrect
                    </Button>
                    <Button
                      onClick={handleCorrect}
                      variant="contained"
                      color="secondary"
                      sx={{ marginLeft: 1, backgroundColor: 'green' }}
                    >
                      Correct
                    </Button>
                  </Box>
                )}
              </>
            ) : (
              <Typography>Nothing to study</Typography>
            )}
          </Box>
        </div>
      ) : (
        <Typography>Nothing to studyefef</Typography>
      )}
    </div>
  );
};

export default Study;
