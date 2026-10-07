import { AppBar, Toolbar, Typography, Box, Button, IconButton, Tooltip } from '@mui/material';
import LocalAtmIcon from '@mui/icons-material/LocalAtm';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import LightModeIcon from '@mui/icons-material/LightMode';
import { useColorMode } from '../../context/ColorModeContext.jsx';
// Every React component must return a single (html) element. In this one, we return an AppBar that acts as a top-level nav bar that contains app title and other nav elements.
// The AppBar is wrapped in a ToolBar to provide proper padding and alignment for its child elements.
// Inside ToolBar we have PrecisionManufacturingIcon and Typography components to display the app icon and title respectively.

//Change out PrecisionManufacturingIcon with a different icon later bc medflow not robopulse

function AppHeader({ username, role, onLogout }) {
    const { mode, toggle } = useColorMode();
    const toggleLabel = mode === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';

    return (
        <AppBar position="static">
            <Toolbar>
                <LocalAtmIcon sx={{ mr: 2 }} />
                <Typography variant="h6" component="h1" sx={{ flexGrow: 1 }}>
                    CashCow Branch Operations Command Center
                </Typography>

                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    {/* Theme toggle: always visible, including on the login screen */}
                    <Tooltip title={toggleLabel}>
                        <IconButton color="inherit" onClick={toggle} aria-label={toggleLabel}>
                            {mode === 'dark' ? <LightModeIcon /> : <DarkModeIcon />}
                        </IconButton>
                    </Tooltip>

                    {/* Username, role and logout only when signed in */}
                    {username && (
                        <>
                            <Typography variant="body2">
                                {username} ({role})
                            </Typography>
                            <Button color="inherit" onClick={onLogout}>
                                Log Out
                            </Button>
                        </>
                    )}
                </Box>
            </Toolbar>
        </AppBar>
    );
}

export default AppHeader;