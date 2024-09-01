import React from 'react';
import Button from '@mui/material/Button';
import { Link } from 'react-router-dom';

interface ButtonRouterProps {
  name: string;
  link: string;
}

const ButtonRouter = ({ name, link }: ButtonRouterProps) => {
  return (
    <Button component={Link} to={link} color="inherit" style={{ padding: '10px' }}>
      {name}
    </Button>
  );
};

export default ButtonRouter;
