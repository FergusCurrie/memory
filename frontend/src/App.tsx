import React, { StrictMode } from 'react';
import { createRoot } from 'react-dom/client'; // Updated import
import { BrowserRouter } from 'react-router-dom';
import { Routes, Route } from 'react-router-dom';
import theme from './components/theme';
import { ThemeProvider } from '@mui/material/styles';
import { Box } from '@mui/material';
import { CssBaseline } from '@mui/material';
import Home from './pages/Home';
import Study from './pages/Study';
import NavigationBar from './pages/NavigationBar';
import AddCards from './pages/AddCards';
import Browse from './pages/Browse';

const App = () => {
  return (
    // <Mindmap />
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        <Box
          sx={{
            backgroundColor: 'background.default',
            height: '100vh',
            width: '100vw',
          }}
        >
          <CssBaseline />
          <NavigationBar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/study" element={<Study />} />
            <Route path="/add_cards" element={<AddCards />} />
            <Route path="/browse" element={<Browse />} />
            {/* <Route path="/mindmap" element={<Mindmap />} />
            <Route path="/train_mindmap" element={<TrainMindmap />} />
            <Route path="/code_train" element={<CodeTrain />} />
            <Route path="/twelve_week_planner" element={<TwelveWeekPlanner />} />
            <Route path="/pdf" element={<PDFPage url="/static/docs/cpumemory.pdf" />} /> */}
            {/* <Route path="/login" element={<Login />} />
            <Route path="/register" element={<RegisterAndLogout />} /> */}
          </Routes>
        </Box>
      </ThemeProvider>
    </BrowserRouter>
  );
};

// const App = () => {
//   return (
//     <h1>TEST</h1>
//   );
// };

// Find the element where you want to mount the React app
const appDiv = document.getElementById('app');
// Check if appDiv exists before trying to create a root
if (appDiv) {
  const root = createRoot(appDiv); // Create a root.
  root.render(<App />); // Use the root to render your App.
}
