import {createTheme} from '@mui/material/styles';

// const theme = createTheme({
//   palette: {
//     primary: {
//       main: '#1976d2',
//     },
//     secondary: {
//       main: '#dc004e',
//     },
//   },
//   shape: {
//     borderRadius: 8,
//   }
// });

// Converting to dark and light mode ability
// Needs to be a function

export function getTheme(mode) {
  return createTheme({
    palette: {
      mode,
      ...(mode === 'light'
        ? { primary: { main: '#1976d2' }, secondary: { main: '#dc004e' } }
        : { primary: { main: '#90caf9' }, secondary: { main: '#f48fb1' } }
      ),
    },
  });
} 
export default getTheme;