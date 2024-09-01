import { createTheme } from '@mui/material/styles';
import { Theme as AugmentedTheme } from '@mui/material/styles';

/*

Typescript requires Module Augmentation. To add myStles they need to be added 
to the ThemeOptions interface, the Theme interface, then in the createTheme

*/

declare module '@mui/material/styles' {
  interface Theme {
    myStyles: {
      dualGrid: any; // Again, replace any with a more specific type as needed
      dualApp?: any;
      dualMatchButtons?: any;
      standardButton?: any;
    };
  }
  // allow configuration using `createTheme`
  interface ThemeOptions {
    myStyles?: {
      dualGrid?: any;
      dualApp?: any;
      dualMatchButtons?: any;
      standardButton?: any;
    };
  }
}

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#556cd6',
      light: '#424242',
      dark: '#87CEEB',
      contrastText: 'blue',
    },
    secondary: {
      main: '#19857b',
    },
    error: {
      main: '#ff1744',
    },
    background: {
      default: 'grey',
      paper: '#ffffff',
    },
    text: {
      primary: '#333333',
      secondary: '#555555',
      disabled: '#aaaaaa',
    },
  },
  myStyles: {
    dualApp: {
      height: '100vh',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      bgcolor: 'background.default',
      color: 'text.primary',
    },
    dualGrid: {
      width: '30vw', // 33% of the viewport width
      height: '30vw', // 33% of the viewport height
      backgroundColor: 'background.default', // Use the theme's primary color
      top: '50%', // Center vertically
      left: '50%', // Center horizontally
      display: 'flex',
      justifyContent: 'center', // Center content horizontally inside the box
      alignItems: 'center',
    },
    dualMatchButtons: {
      display: 'flex',
      gap: 2,
    },
    standardButton: {
      color: 'primary.medium',
    },
  },
});

export default theme;

/*
import { useTheme } from '@mui/material';
const theme = useTheme();
sx={theme.myStyles.dualApp}

function getRandomColor() {
  const letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}
*/
