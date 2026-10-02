import { useEffect, useState } from 'react';
const LOW_CASH_THRESHOLD = 20; // Example threshold value for low cash
import { DataGrid } from '@mui/x-data-grid';
import { Alert, Box, CircularProgress } from '@mui/material';
import apiClient from '../../api/client.js';

//defines our DataGrid columns and maps them to our backend API response data
const columns = [
  { field: 'id', headerName: 'ID', width: 70 },
  { field: 'serial_number', headerName: 'Serial Number', width: 150 },
  { field: 'model', headerName: 'Model', width: 160 },
  { field: 'cash_level', headerName: 'Cash %', width: 120, type: 'number' },
  { field: 'status', headerName: 'Status', width: 130 },
  { field: 'branch_id', headerName: 'Branch ID', width: 110, type: 'number' },
];

//local state variables for tracking table rows, loading status, and network errors
//to track the lifecycle of the async API request so the UI can render appropriately
function LowCashDataGrid() {
  const [atm, setATM] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  //React effect hook that runs our async fetch 
  useEffect(() => {
    //tracks component mount status to prevent memory leaks via network request delays
    let isMounted = true;

    //pulls our ATM data from the backend
    async function fetchATM() {
      try {
        const response = await apiClient.get('/atm', {params: {max_cash: LOW_CASH_THRESHOLD}});
        if (isMounted) setATM(response.data);
      } catch (err) {
        console.error('ATM fetch failed:', err);
        if (isMounted) setError('Could not load ATM data.');
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    fetchATM();

    return () => {
      isMounted = false;
    };
  }, []);

  //shows a spinning progress indicator if loading data
  if (loading) return <CircularProgress />;
  //shows error alert if API call fails
  if (error) return <Alert severity="error">{error}</Alert>;

  //loads data grid component if all goes well
  return (
    <Box sx={{ height: 400, width: '100%' }}>
      <DataGrid rows={atm} columns={columns} getRowId={(row) => row.id} />
    </Box>
  );
}

export default LowCashDataGrid;