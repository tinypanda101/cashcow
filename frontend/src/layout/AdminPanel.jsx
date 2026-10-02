import { useState } from 'react';
import { Container, Typography, Box } from '@mui/material';

import CRUDActions from "../components/adminpanel/CRUDActions.jsx"
function AdminPanel() {
  
  const [userRefreshKey, setUserRefreshKey] = useState(0);

  return (
    <Container maxWidth='lg' sx={{ mt: 4 }}>
      <CRUDActions />
    </Container>
  );
}

export default AdminPanel;