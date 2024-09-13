import React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Box from '@mui/material/Box';
import MenuIcon from '@mui/icons-material/Menu';
import ButtonRouter from '../components/ButtonRouter';

const NavigationBar = () => {
  return (
    <Box>
      <AppBar position="static">
        <Toolbar>
          <IconButton size="large" edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }}>
            <MenuIcon />
          </IconButton>
          <ButtonRouter name="HOME" link="/" />
          <ButtonRouter name="FLASHCARDS  " link="/study" />
          <ButtonRouter name="ADD cards  " link="/add_cards" />
          <ButtonRouter name="browse" link="/browse" />
          <ButtonRouter name="Add Code" link="/add_code" />
          {/* <ButtonRouter name="MINDMAP" link="/mindmap" />
          <ButtonRouter name="TRAIN_MIND_MAP" link="/train_mindmap" />
          <ButtonRouter name="CODE_TRAIN" link="/code_train" />
          <ButtonRouter name="12 WEEK PLAN" link="/twelve_week_planner" />
          <ButtonRouter name="PDF reader like andy" link="/pdf" />
          <div style={{ flexGrow: 1 }}></div> {/* Spacer element */}
        </Toolbar>
      </AppBar>
    </Box>
  );
};

export default NavigationBar;
