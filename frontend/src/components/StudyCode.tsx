import React, { useState, useEffect, useRef } from 'react';
import {
  Button,
  Card,
  CardContent,
  Typography,
  Box,
  Table,
  TableHead,
  TableCell,
  TableRow,
  TableContainer,
  TableBody,
  Paper,
  CircularProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import api from '../api';
import Editor, { OnMount } from '@monaco-editor/react';
import PandasJsonTable from './PandasTable';
import { KeyboardEvent } from 'react';

interface CodeCard {
  id: number;
  note_id: number;
  dataset_name: string;
  problem_description: string;
  code: string;
  dataset_header: string;
}

const StudyCode: React.FC = () => {
  const [cards, setCards] = useState<CodeCard[]>([]);
  const [currentCard, setCurrentCard] = useState<CodeCard | null>(null);
  const [showAnswer, setShowAnswer] = useState(false);
  const [editorContent, setEditorContent] = useState<string>('result = (\n\tdf\n\n)');
  const [submittedResult, setSubmittedResult] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [testPassed, setTestPassed] = useState<boolean | null>(null);
  const [tableHeader, setTableHeader] = useState<Record<string, any> | null>(null);
  const [codeError, setCodeError] = useState<string>('');
  const [openAnswerDialog, setOpenAnswerDialog] = useState(false);

  useEffect(() => {
    fetchCards();
  }, []);

  const fetchCards = async () => {
    try {
      const response = await api.get('/api/code/code_to_review');
      console.log(response);
      setCards(response.data.codes);
      pickRandomCard(response.data.codes);
    } catch (error) {
      console.error('Error fetching code cards:', error);
    }
  };

  // const getHeader = async () => {
  //   console.log(cards);
  //   console.log(currentCard?.dataset_name);
  //   try {
  //     const response = await api.get('/api/code/get_data_header', {
  //       params: { dataset_name: currentCard?.dataset_name },
  //     });
  //     setTableHeader(JSON.parse(response.data.header));
  //   } catch (error) {
  //     console.error('Error fetching code cards:', error);
  //   }
  // };

  const pickRandomCard = (cardArray: CodeCard[]) => {
    if (cardArray.length > 0) {
      const randomIndex = Math.floor(Math.random() * cardArray.length);
      setCurrentCard(cardArray[randomIndex]);
      //console.log(currentCard);

      // getHeader();
      setShowAnswer(false);
    } else {
      setCurrentCard(null);
    }
  };

  const handleScore = async (result: boolean) => {
    if (currentCard) {
      try {
        console.log({
          code_id: currentCard.id,
          result: result,
        });
        await api.post('/api/code/reviews', {
          code_id: currentCard.id,
          result: result,
        });
        setCards((prevCards) => prevCards.filter((card) => card.id !== currentCard.id));
        pickRandomCard(cards.filter((card) => card.id !== currentCard.id));
      } catch (error) {
        console.error('Error submitting review:', error);
      }
    }
  };

  const handleSendCode = async () => {
    const currentContent = editorRef.current?.getValue() || editorContent;
    console.log('Sending code:', currentContent);
    setIsLoading(true);
    try {
      const response = await api.post('/api/code/submit_code', {
        code: currentContent,
        code_id: currentCard?.id,
      });
      console.log('API response:', response);
      setSubmittedResult(JSON.parse(response.data.result_head));
      setTestPassed(response.data.passed);
      setCodeError(response.data.error);
      console.log(response);
      console.log('Code submitted successfully');
    } catch (error) {
      console.error('Error submitting code:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEditorDidMount: OnMount = (editor, monaco) => {
    editorRef.current = editor;
    editor.addCommand(monaco.KeyMod.Shift | monaco.KeyCode.Enter, () => {
      handleSendCode();
    });
  };

  const editorRef = useRef<any>(null);

  const handleEditorChange = (value: string | undefined) => {
    setEditorContent(value || '');
  };

  const handleEditorKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    if (event.key === 'Enter' && event.shiftKey) {
      event.preventDefault();
      handleSendCode();
    }
  };

  const handleOpenAnswerDialog = () => {
    setOpenAnswerDialog(true);
  };

  const handleCloseAnswerDialog = () => {
    setOpenAnswerDialog(false);
  };

  if (!currentCard) {
    return <Typography>All done with code cards!</Typography>;
  }

  return (
    <>
      <Card>
        <CardContent>
          <Typography variant="h5" component="div" gutterBottom>
            Description:
          </Typography>
          <Typography variant="body1" paragraph>
            {currentCard.problem_description}
          </Typography>

          {/* {showAnswer && (
            <>
              <Typography variant="h5" component="div" gutterBottom>
                Resulting Dataframe:
              </Typography>
              <Typography variant="body1" paragraph>
                {currentCard.resulting_dataframe}
              </Typography>
            </>
          )} */}
        </CardContent>
      </Card>
      <Box sx={{ mt: 4, mb: 4 }}></Box>
      {currentCard && (
        <PandasJsonTable data={JSON.parse(currentCard.dataset_header)}></PandasJsonTable>
      )}

      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h5" component="div" gutterBottom>
          Code Editor:
        </Typography>
        <Editor
          height="300px"
          defaultLanguage="python"
          value={editorContent}
          onChange={handleEditorChange}
          options={{
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            fontSize: 14,
          }}
          onMount={handleEditorDidMount}
        />
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
          <Button variant="contained" color="primary" onClick={handleSendCode} disabled={isLoading}>
            {isLoading ? <CircularProgress size={24} /> : 'Submit Code'}
          </Button>
          <Button variant="contained" color="primary" onClick={handleOpenAnswerDialog}>
            Show Answer
          </Button>
        </Box>
      </Box>
      <Typography>{codeError}</Typography>
      {submittedResult && (
        <Box sx={{ mt: 4, mb: 4 }}>
          <Typography variant="h5" component="div" gutterBottom>
            Submitted Result:
          </Typography>
          <Alert severity={testPassed ? 'success' : 'error'} sx={{ mb: 2 }}>
            {testPassed ? 'Test Passed' : 'Test Failed'}
          </Alert>
          <PandasJsonTable data={submittedResult} />
        </Box>
      )}
      <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-between' }}>
        <Button
          variant="contained"
          color="error"
          onClick={() => handleScore(false)}
          sx={{ flex: 1, mr: testPassed ? 1 : 0 }}
        >
          Incorrect
        </Button>
        {testPassed && (
          <Button
            variant="contained"
            color="success"
            onClick={() => handleScore(true)}
            sx={{ flex: 1, ml: 1 }}
          >
            Correct
          </Button>
        )}
      </Box>
      <Box sx={{ mt: 2, display: 'flex', justifyContent: 'center' }}>
        <Button variant="contained" color="primary" onClick={fetchCards} sx={{ mt: 2 }}>
          Get New Random Card
        </Button>
      </Box>

      <Dialog open={openAnswerDialog} onClose={handleCloseAnswerDialog}>
        <DialogTitle>Answer</DialogTitle>
        <DialogContent>
          <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>{currentCard?.code}</pre>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseAnswerDialog}>Close</Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default StudyCode;
