import { createContext, useCallback, useContext, useMemo, useState } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import useMediaQuery from '@mui/material/useMediaQuery';
import { getTheme } from '../theme';

const STORAGE_KEY = 'cashcow-color-mode';
const ColorModeContext = createContext(null);

function readStored() {
    try {
        const stored = window.localStorage.getItem(STORAGE_KEY);
        return stored === 'light' || stored === 'dark' ? stored : null;
    } catch {
        return null; // nothing stored so do system pref
    }
}

function writeStored(mode) {
    try {window.localStorage.setItem(STORAGE_KEY, mode);} catch {}
}

export function ColorModeProvider({ children }) {
    const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');
    const [stored, setStored] = useState(readStored);
    const mode = stored ?? (prefersDarkMode ? 'dark' : 'light');

    const toggle = useCallback(() => {
        const next = mode === 'dark' ? 'light' : 'dark';
        setStored(next);
        writeStored(next);
    }, [mode]);
    const theme = useMemo(() => getTheme(mode), [mode]);
  const value = useMemo(() => ({ mode, toggle }), [mode, toggle]);

  return (
    <ColorModeContext.Provider value={value}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

export const useColorMode = () => useContext(ColorModeContext);