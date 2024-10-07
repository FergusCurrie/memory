import { Editor } from '@monaco-editor/react';
import { Alert, Box, Button, Card, CardContent, Typography } from '@mui/material';
import React, { useState, useEffect, useRef } from 'react';
import api from '../../api';
import PandasJsonTable from './PandasTable';

interface CodeEditorProps {
  problem_id?: number;
  testPassed: boolean;
  setTestPassed: React.Dispatch<React.SetStateAction<boolean>>;
  code_default: string;
}

const CodeEditor: React.FC<CodeEditorProps> = ({
  problem_id,
  testPassed,
  setTestPassed,
  code_default,
}) => {
  const editorRef = useRef<any>(null);
  const [editorContent, setEditorContent] = useState<string>(
    code_default || 'result = (\n\tdf\n\n)',
  );
  const [submittedResult, setSubmittedResult] = useState<any>(null);
  const [codeError, setCodeError] = useState<string>('');
  useEffect(() => {
    setSubmittedResult(null);
    setCodeError('');
  }, [problem_id]);

  const handleSendCode = async () => {
    const currentContent = editorRef.current?.getValue() || editorContent;
    try {
      const payload = {
        code: currentContent,
        problem_id: problem_id,
      };
      const response = await api.post('/api/code/test_code', payload);
      setSubmittedResult(JSON.parse(response.data.result_head));
      setTestPassed(response.data.passed);
      setCodeError(response.data.error);
      console.log('Code submitted successfully');
    } catch (error) {
      console.error('Error submitting code:', error);
    }
    // } finally {
    //   setIsLoading(false);
    // }
  };

  const handleEditorChange = (value: string | undefined) => {
    setEditorContent(value || '');
  };

  return (
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
        // onMount={handleEditorDidMount}
      />
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
        <Button variant="contained" color="primary" onClick={handleSendCode}>
          'Submit Code'
        </Button>
        {/* <Button variant="contained" color="primary" onClick={handleOpenAnswerDialog}>
          Show Answer
        </Button> */}
      </Box>
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
      <Typography>{codeError}</Typography>
    </Box>
  );
};

export default CodeEditor;
